import matplotlib.pyplot as plt
import numpy as np
import os
from models.dataset import DatasetModel
from models.version import VersionModel
from models.object import ObjectModel
from models.version_object import VersionObjectModel
from sqlalchemy import func, desc
from sqlalchemy.orm import load_only
from schemas.dataset.responses.dataset_response import DatasetResponse
from services.alerce_database_service import AlerceDatabaseService
from utils.sql_queries import FEATURES_QUERY, FEATURES_VALUES_QUERY, SELECT_DETECTION


def plot_diffLC(oid, LC_det, LC_nondet, save_path):
    fig, ax = plt.subplots(figsize=(14, 8))
    labels = {1: "g", 2: "r"}
    colors = {1: "#56E03A", 2: "#D42F4B"}
    markers = {1: "o", 2: "s"}

    # loop the passbands
    for fid in [1, 2]:
        # plot detections if available
        mask = LC_det.fid == fid
        if np.sum(mask) > 0:
            # note that the detections index is candid and that we are plotting the psf corrected magnitudes
            ax.errorbar(
                LC_det[mask].mjd,
                LC_det[mask].magpsf,
                yerr=LC_det[mask].sigmapsf,
                c=colors[fid],
                fmt=markers[fid],
                label=labels[fid],
            )

        # plot non detections if available and if wanted:
        mask = (LC_nondet.fid == fid) & (LC_nondet.diffmaglim > -900)
        if np.sum(mask) > 0:
            # non detections index is mjd
            ax.scatter(
                LC_nondet[mask].mjd,
                LC_nondet[mask].diffmaglim,
                c=colors[fid],
                alpha=0.5,
                marker="v",
                label="lim.mag. %s" % labels[fid],
            )

    ax.set_title(oid)
    ax.set_xlabel("MJD")
    ax.set_ylabel("difference magnitude")
    ax.legend()
    ax.set_ylim(ax.get_ylim()[::-1])
    plt.savefig(save_path + "/" + oid + ".png")
    plt.close()


def make_folder(*args):
    folder_path = os.path.join(*args)
    try:
        os.makedirs(folder_path)
        print("Directory '%s' created successfully" % folder_path)
    except OSError as error:
        print("Directory '%s' can not be created" % folder_path)

    return folder_path


def sql_query_handler(db_conn, query, params, dataset_path, folder_name, file_path):
    data = db_conn.execute_query(query, params)
    data_path = make_folder(dataset_path, folder_name)
    data.to_csv(data_path + file_path, index=False)
    return data


def get_dataset_responses(db, dataset_models):
    last_version_list = []

    for dataset in dataset_models:
        last_version = (
            db.query(VersionModel.num)
            .filter(VersionModel.did == dataset.did)
            .order_by(desc(VersionModel.num))
            .limit(1)
        )

        last_version_list.append(last_version[0][0])

    dataset_responses = []

    for i in range(len(dataset_models)):
        dataset_response = DatasetResponse(
            did=dataset_models[i].did,
            name=dataset_models[i].name,
            author=dataset_models[i].author,
            create_date=dataset_models[i].create_date,
            last_update=dataset_models[i].last_update,
            last_version=last_version_list[i],
        )
        dataset_responses.append(dataset_response)

    return dataset_responses


# metodo para comparar jsons con el mismo contenido pero desordenado de distinta forma
def ordered_json(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered_json(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered_json(x) for x in obj)
    else:
        return obj


def get_feature_versions(oids):
    AlerceDatabaseService.initialize_connection_pool()
    feature_versions_df = AlerceDatabaseService.execute_query(
        FEATURES_QUERY, params={"oids": oids}
    )

    feature_versions = feature_versions_df["version"].values.tolist()

    return feature_versions


def get_features_values(oids, feature_names):
    AlerceDatabaseService.initialize_connection_pool()
    features_values_df = AlerceDatabaseService.execute_query(
        FEATURES_VALUES_QUERY, params={"oids": oids, "features": feature_names}
    )

    return features_values_df


def get_detections(oids):
    AlerceDatabaseService.initialize_connection_pool()
    detections_df = AlerceDatabaseService.execute_query(
        SELECT_DETECTION, params={"oids": oids}
    )

    return detections_df


def get_oids_version(db, vid):
    oids_version = (
        db.query(VersionObjectModel.objects)
        .filter(VersionObjectModel.versions == vid)
        .all()
    )
    oids_version = [item[0] for item in oids_version]

    return oids_version


def add_new_dataset(db, dataset_info):
    new_dataset = DatasetModel(
        name=dataset_info.name,
        author=dataset_info.author,
        description=dataset_info.description,
        parent_did=dataset_info.parent_did,
        create_date=func.now(),
        last_update=func.now(),
    )

    db.add(new_dataset)
    db.commit()

    return new_dataset


def add_new_version(
    db, version_num, dataset_id, feature_versions, json_specs, collaborator
):
    new_version = VersionModel(
        num=version_num,
        did=dataset_id,
        version_date=func.now(),
        specs=json_specs,
        feature_versions=feature_versions,
        collaborator=collaborator,
    )

    db.add(new_version)
    db.commit()

    return new_version


def add_new_oids_to_db(db, new_oids):
    oids_in_db = db.query(ObjectModel.oid).all()

    oids_in_db = [item[0] for item in oids_in_db]

    for oid in new_oids:
        if oid not in oids_in_db:
            new_oid = ObjectModel(oid=oid)
            db.add(new_oid)

    db.commit()


def link_oids_to_version(db, version_id, oids):
    for oid in oids:
        version_oid = VersionObjectModel(versions=version_id, objects=oid)
        db.add(version_oid)
    db.commit()


def change_dataset_name(db, did, name):
    db.query(DatasetModel).filter(DatasetModel.did == did).update(
        {
            DatasetModel.name: name,
        }
    )
    db.commit()


def change_dataset_description(db, did, description):
    db.query(DatasetModel).filter(DatasetModel.did == did).update(
        {
            DatasetModel.description: description,
        }
    )
    db.commit()


def delete_oids_from_version_in_db(db, version_id, oids_to_delete):
    deleted_objects = (
        db.query(VersionObjectModel.objects)
        .filter(VersionObjectModel.versions == version_id)
        .filter(VersionObjectModel.objects.in_(oids_to_delete))
        .all()
    )

    deleted_objects = [obj[0] for obj in deleted_objects]

    db.query(VersionObjectModel).filter(
        VersionObjectModel.versions == version_id
    ).filter(VersionObjectModel.objects.in_(oids_to_delete)).delete()

    db.commit()

    return deleted_objects


def remove_duplicates_with_sets(list1, list2):
    set1 = set()
    set2 = set()

    if list1 != None:
        set1 = set(list1)
    if list2 != None:
        set2 = set(list2)

    common_elements = set1.intersection(set2)
    set1 -= common_elements
    set2 -= common_elements

    list1 = list(set1)
    list2 = list(set2)

    return list1, list2


def compare_and_update_specs(
    db,
    did,
    update_input,
    current_version_num,
    current_version_vid,
    current_specs,
    update_specs,
):
    new_version = None
    specs_changed = False

    if ordered_json(current_specs) != ordered_json(update_specs):
        oids_current_version = get_oids_version(db, current_version_vid)
        feature_versions = get_feature_versions(oids_current_version)

        new_version = add_new_version(
            db=db,
            version_num=current_version_num + 1,
            dataset_id=did,
            feature_versions=feature_versions,
            json_specs=update_input.specs.model_dump_json(),
            collaborator=update_input.collaborator,
        )

        current_version_num = new_version.num
        current_version_vid = new_version.vid

        link_oids_to_version(db, current_version_vid, oids_current_version)

        specs_changed = True

    return new_version, current_version_num, current_version_vid, specs_changed


def add_oids_to_version(
    db,
    new_version,
    oids_to_add_in_dataset,
    did,
    current_version_vid,
    current_version_num,
    update_input,
):
    new_oids = []

    if len(oids_to_add_in_dataset) != 0:
        oids_current_version = get_oids_version(db, current_version_vid)

        new_oids = [
            oid for oid in oids_to_add_in_dataset if oid not in oids_current_version
        ]

        if len(new_oids) != 0:
            add_new_oids_to_db(db, new_oids)

            current_and_new_oids = oids_current_version + new_oids
            feature_versions = get_feature_versions(current_and_new_oids)

            if new_version is None:
                new_version = add_new_version(
                    db=db,
                    version_num=current_version_num + 1,
                    dataset_id=did,
                    feature_versions=feature_versions,
                    json_specs=update_input.specs.model_dump_json(),
                    collaborator=update_input.collaborator,
                )

                current_version_num = new_version.num
                current_version_vid = new_version.vid

                link_oids_to_version(db, current_version_vid, current_and_new_oids)

            else:
                new_version.feature_versions = feature_versions
                db.commit()
                link_oids_to_version(db, current_version_vid, new_oids)

    return new_version, current_version_num, current_version_vid, new_oids


def delete_oids_from_version(
    db,
    oids_to_delete_in_dataset,
    did,
    update_input,
    current_version_vid,
    current_version_num,
    new_version,
):
    deleted_oids = []

    if len(oids_to_delete_in_dataset) != 0:
        # hay un error que no corregire por ahora, tengo que considerar que almenos
        # quede un oid en la version actual o en la nueva version, por el momento
        # se pueden borrar todos los oids y dejar una version sin oids.

        if new_version is None:
            oids_current_version = get_oids_version(db, current_version_vid)

            kept_oids = [
                oid
                for oid in oids_current_version
                if oid not in oids_to_delete_in_dataset
            ]

            if len(kept_oids) >= 1 and len(kept_oids) != len(oids_current_version):
                deleted_oids = [
                    oid for oid in oids_current_version if oid not in kept_oids
                ]

                feature_versions = get_feature_versions(kept_oids)

                print(f"features en delete1 {feature_versions}")

                new_version = add_new_version(
                    db=db,
                    version_num=current_version_num + 1,
                    dataset_id=did,
                    feature_versions=feature_versions,
                    json_specs=update_input.specs.model_dump_json(),
                    collaborator=update_input.collaborator,
                )

                current_version_num = new_version.num
                current_version_vid = new_version.vid

                link_oids_to_version(db, current_version_vid, kept_oids)

        else:
            deleted_oids = delete_oids_from_version_in_db(
                db, current_version_vid, oids_to_delete_in_dataset
            )

            oids_current_version = get_oids_version(db, current_version_vid)
            feature_versions = get_feature_versions(oids_current_version)

            print(f"features en delete2 {feature_versions}")

            new_version.feature_versions = feature_versions
            db.commit()

    return current_version_num, deleted_oids
