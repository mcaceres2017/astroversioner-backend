# general
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc, func, update, and_
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from typing import List
import json
import zipfile
import pandas as pd
import io
from models.user import UserModel
from schemas.dataset.responses.dataset_general import DatasetGeneralInformation
from schemas.dataset.responses.update_information import UpdateInformation

# services
from services.alerce_database_service import AlerceDatabaseService
from services.alerce_stamp_service import AlerceStampService

# pydantic schemas
from schemas.dataset.input.dataset_information import DatasetInformation
from schemas.dataset.responses.dataset_response import DatasetResponse
from schemas.dataset.input.dataset_update import DatasetUpdate
from schemas.dataset.responses.metadata_response import MetadataResponse
from schemas.dataset.specifications import Specifications
from schemas.dataset.responses.version_response import VersionResponse
from schemas.dataset.responses.dataset_creation_response import (
    DatasetCreationResponse,
)
from schemas.dataset.responses.dataset_update_response import DatasetUpdateResponse

# sql alchemy models
from models.dataset import DatasetModel
from models.object import ObjectModel
from models.version_object import VersionObjectModel
from models.version import VersionModel

# database
from database.db_connector import get_db

# utils
from utils.sql_queries import FEATURES_QUERY
from utils.utils import (
    ordered_json,
    add_new_dataset,
    get_feature_versions,
    add_new_version,
    add_new_oids_to_db,
    link_oids_to_version,
    change_dataset_name,
    change_dataset_description,
    get_oids_version,
    delete_oids_from_version,
    get_dataset_responses,
    get_features_values,
    get_detections,
    remove_duplicates_with_sets,
    compare_and_update_specs,
    add_oids_to_version,
)


dataset_router = APIRouter()


@dataset_router.get("/", response_model=List[DatasetResponse])
async def get_all_datasets(db: Session = Depends(get_db)):
    """
    Description: Get all datasets.
    Parameters: None.
    Returns: Empty response.
    """
    dataset_models = db.query(DatasetModel).all()

    return get_dataset_responses(db, dataset_models)


# Endpoint to retrieve all the datasets of a specific user
@dataset_router.get("/{user}", response_model=List[DatasetResponse])
async def dataset_user_get(user: str, db: Session = Depends(get_db)):
    """
    Description: Retrieves the datasets where an user is the author.
    Parameters:
        - user (str): Username.
    Returns: Empty response.
    """

    user_datasets = db.query(DatasetModel).filter(DatasetModel.author == user).all()

    return get_dataset_responses(db, user_datasets)


# Endpoint to get the information for a specific version of a given dataset
@dataset_router.get("/{did}/version/{version}", response_model=VersionResponse)
async def get_version_info(did: int, version: int, db: Session = Depends(get_db)):
    version_model = (
        db.query(VersionModel)
        .filter(VersionModel.did == did)
        .filter(VersionModel.num == version)
        .first()
    )

    oids = (
        db.query(VersionObjectModel.objects)
        .filter(VersionObjectModel.versions == version_model.vid)
        .all()
    )

    oid_list = [item[0] for item in oids]

    version_specs = json.loads(version_model.specs)
    version_specs = Specifications(**version_specs)

    response = VersionResponse(
        collaborator=version_model.collaborator,
        version_date=version_model.version_date.strftime("%d-%m-%Y"),
        specs=version_specs,
        oids=oid_list,
    )

    return response


# Endpoint to get the general information of a dataset that is common to all versions
@dataset_router.get("/{did}/metadata", response_model=MetadataResponse)
async def get_dataset_metadata(did: int, db: Session = Depends(get_db)):
    versions = db.query(VersionModel.num).filter(VersionModel.did == did).all()
    versions = [v[0] for v in versions]

    dataset = db.query(DatasetModel).filter(DatasetModel.did == did).first()

    parent_did = None
    parent_did_name = None

    if dataset.parent_did != None:
        parent_did = dataset.parent_did
        parent_did_name = (
            db.query(DatasetModel.name).filter(DatasetModel.did == parent_did).first()
        )
        parent_did_name = parent_did_name[0]

    response = MetadataResponse(
        name=dataset.name,
        versions=versions,
        description=dataset.description,
        create_date=dataset.create_date.strftime("%d-%m-%Y"),
        author=dataset.author,
        parent_did=parent_did,
        parent_did_name=parent_did_name,
    )

    return response


@dataset_router.post("/{did}/update", response_model=DatasetUpdateResponse)
async def update_dataset(
    did: int, update_input: DatasetUpdate, db: Session = Depends(get_db)
):
    dataset = db.query(DatasetModel).filter(DatasetModel.did == did).first()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    user = (
        db.query(UserModel)
        .filter(UserModel.username == update_input.collaborator)
        .first()
    )

    if not user:
        raise HTTPException(status_code=404, detail="The collaborator doesn't exist")

    current_version = (
        db.query(VersionModel)
        .filter(VersionModel.did == did)
        .order_by(desc(VersionModel.num))
        .limit(1)
    )

    current_version_num = current_version[0].num
    current_version_vid = current_version[0].vid

    current_specs = json.loads(current_version[0].specs)
    update_specs = json.loads(update_input.specs.model_dump_json())

    response = DatasetUpdateResponse(success=False, message="")
    updated_information = UpdateInformation(
        did=did,
        name=dataset.name,
        description=dataset.description,
        old_version=current_version_num,
        new_version=current_version_num,
        specs=None,
        added_oids=[],
        deleted_oids=[],
    )

    if dataset.name != update_input.name:
        change_dataset_name(db, did, update_input.name)
        updated_information.name = update_input.name
        response.message += "name updated,"

    if dataset.description != update_input.description:
        change_dataset_description(db, did, update_input.description)
        updated_information.description = update_input.description
        response.message += "description updated,"

    (
        new_version,
        current_version_num,
        current_version_vid,
        specs_changed,
    ) = compare_and_update_specs(
        db,
        did,
        update_input,
        current_version_num,
        current_version_vid,
        current_specs,
        update_specs,
    )

    if specs_changed:
        response.message += "specs updated,"
        updated_information.specs = Specifications(
            **json.loads(update_input.specs.model_dump_json())
        )

    oids_to_add_in_dataset, oids_to_delete_in_dataset = remove_duplicates_with_sets(
        update_input.oids_add, update_input.oids_delete
    )

    (
        new_version,
        current_version_num,
        current_version_vid,
        added_oids,
    ) = add_oids_to_version(
        db,
        new_version,
        oids_to_add_in_dataset,
        did,
        current_version_vid,
        current_version_num,
        update_input,
    )

    if len(added_oids) != 0:
        response.message += "oids added,"
        updated_information.added_oids = added_oids

    current_version_num, deleted_oids = delete_oids_from_version(
        db,
        oids_to_delete_in_dataset,
        did,
        update_input,
        current_version_vid,
        current_version_num,
        new_version,
    )

    if len(deleted_oids) != 0:
        response.message += "oids deleted,"
        updated_information.deleted_oids = deleted_oids

    updated_information.new_version = current_version_num

    if response.message != "":
        response.success = True

    else:
        response.message = "no change was detected"

    response.updated_dataset = updated_information

    return response


# Endpoint to download a specific version of a dataset.
@dataset_router.get("/{did}/version/{version}/download")
async def dataset_download_get(did: int, version: int, db: Session = Depends(get_db)):
    """
    Description: Download a specific dataset by its ID.
    Parameters:
        - did (int): ID of the dataset to download.
        - version (int): the specific version of the dataset.
    Returns: Empty response.
    """

    dataset_info = db.query(DatasetModel).filter(DatasetModel.did == did).first()

    dataset_name = dataset_info.name

    zip_name = dataset_name + "_version_" + str(version)

    version_info = (
        db.query(VersionModel)
        .filter(VersionModel.did == did)
        .filter(VersionModel.num == version)
        .first()
    )

    specs = json.loads(version_info.specs)
    oids_version = get_oids_version(db, version_info.vid)

    zip_buffer = io.BytesIO()

    feature_df_content = []
    image_data_list = []
    stamp_names = []

    if specs["features"]:
        print("esta sacando las features")

        # con esto el df queda listo para cargarlo al futuro zip.
        feature_values_df = get_features_values(oids_version, specs["features"])

        # extrayendo el contenido del df en binario o en bytes.
        string_io = io.StringIO()
        feature_values_df.to_csv(string_io, index=False)

        feature_df_content = string_io.getvalue()

    if specs["stamps"]:
        print("esta sacando las stamps")
        detections_df = get_detections(oids_version)

        # con esto las imagenes se pueden cargar al futuro zip.
        image_data_list, stamp_names = AlerceStampService.get_stamps_as_images(
            detections_df
        )

        # print(f"una muestra del image_data_list: {image_data_list[0:3]}")
        # print(f"y los nombres asociados: {stamp_names[0:3]}")

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED, False) as zip_file:
        # cargando imagenes al zip
        for i in range(len(stamp_names)):
            zip_file.writestr("images/" + stamp_names[i], image_data_list[i])

        # cargando csv al zip
        if feature_df_content:
            zip_file.writestr("features/features.csv", feature_df_content)

        zip_buffer.seek(0)

    # ojo que asi como esta el codigo, podria devolver zips con cero bytes.
    # de algun modo hay que checkear si tiene contenido adentro antes de
    # hacer streaming.
    return StreamingResponse(
        io.BytesIO(zip_buffer.getvalue()),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment;filename=" + zip_name + ".zip"},
    )


@dataset_router.post("/", response_model=DatasetCreationResponse)
async def dataset_post(dataset_info: DatasetInformation, db: Session = Depends(get_db)):
    """
    Description: Stores the necessary information for the
    recreation of a dataset in the database.
    Parameters: None.
    Returns: Empty response.
    """

    dataset = (
        db.query(DatasetModel).filter(DatasetModel.name == dataset_info.name).first()
    )

    user = db.query(UserModel).filter(UserModel.username == dataset_info.author).first()

    if not user:
        raise HTTPException(status_code=404, detail="The user doesn't exist")

    if not dataset:
        new_dataset = add_new_dataset(db, dataset_info)

        feature_versions = get_feature_versions(dataset_info.oids)

        add_new_version(
            db=db,
            dataset_id=new_dataset.did,
            feature_versions=feature_versions,
            json_specs=dataset_info.specs.model_dump_json(),
            collaborator=dataset_info.author,
            version_num=1,
        )

        add_new_oids_to_db(db, dataset_info.oids)

        #################
        #################

        vid = (
            db.query(VersionModel.vid)
            .filter(VersionModel.did == new_dataset.did)
            .filter(VersionModel.num == 1)
            .first()
        )

        link_oids_to_version(db, vid[0], dataset_info.oids)

        dataset_general_info = DatasetGeneralInformation(
            did=new_dataset.did,
            name=new_dataset.name,
            version=1,
            author=new_dataset.author,
        )

        return DatasetCreationResponse(
            success=True,
            message="Dataset created successfully.",
            dataset=dataset_general_info,
        )

    else:
        raise HTTPException(status_code=404, detail="Dataset name already exist")
