
# Astroversioner 

This repository contains the source code of the service api of the astroversioner system, which is in charge of the maintenance and versioning of multimodal datasets within the context of the ALeRCE project.



## Run Locally

Clone the project

```bash
  git clone https://github.com/mcaceres2017/astroversioner.git
```

Go to the project directory

```bash
  cd my-project
```

Create a virtual enviroment

```bash
  python -m venv my-project
```

Install requirements

```bash
  pip install -r requirements.txt
```

Activate the virtual enviroment

```bash
  source my-project/env/bin/activate
```

Run uvicorn server

```bash
  uvicorn main:app --host 0.0.0.0 --port 8000
```






## Demo

The functional version of this api can be accessed via the following link:

- [Astroversioner API](https://astrocollab.inf.udec.cl/versioner)


## Platform Astroversioner
To access the platform that consumes this api you can access through the following links:

WORK IN PROGRESS

## API Reference

#### Get_all_datasets

```http
  GET /versioner/dataset
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| - | - | - |

#### Body

```json

```

#### Response

```json
  [
    
    {
      "did":1,
      "name":"Dataset que sera modificado",
      "author":"asanchez2017",
      "create_date":"2024-01-03",
      "last_update":"2024-01-03",
      "last_version":1
    },
    {
      "did":2,
      "name":"Dataset que sera modificado2",
      "author":"mcaceres2017",
      "create_date":"2024-01-03",
      "last_update":"2024-01-03",
      "last_version":1
    },
  ]
```


#### Get user's datasets

```http
  GET /versioner/dataset/{user}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `user`      | `string` | **Required**. owner of datasets |

#### Body

```json

```

#### Response

```json
  [
    
    {
      "did":1,
      "name":"Dataset que sera modificado",
      "author":"asanchez2017",
      "create_date":"2024-01-03",
      "last_update":"2024-01-03",
      "last_version":1
    },
    {
      "did":2,
      "name":"Dataset que sera modificado2",
      "author":"asanchez2017",
      "create_date":"2024-01-03",
      "last_update":"2024-01-03",
      "last_version":1
    },
  ]
```



#### Get dataset metadata 

```http
  GET /versioner/dataset/{did}/metadata
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `did`      | `integer` | **Required**. dataset index |

#### Body

```json

```

#### Response

```json
  {
    "name": "Dataset que sera modificado",
    "versions": [
        1
    ],
    "description": "test test test",
    "create_date": "03-01-2024",
    "author": "asanchez2017",
    "parent_did": null,
    "parent_did_name": null
  } 
```


#### Get dataset version 

```http
  GET /versioner/dataset/{did}/version/{version}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `did`      | `integer` | **Required**. dataset index |
| `version`      | `integer` | **Required**. version number |

#### Body

```json

```

#### Response

```json
  {
    "collaborator": "asanchez2017",
    "version_date": "03-01-2024",
    "specs": {
        "det": false,
        "non_det": false,
        "lc": false,
        "xmatch": false,
        "features": [
            "gal_l",
            "GP_DRW_sigma",
            "GP_DRW_tau",
            "g-r_max",
            "g-r_max_corr",
            "g-r_mean",
            "g-r_mean_corr",
            "Gskew",
            "g-W2",
            "g-W3",
            "Harmonics_mag_1",
            "Harmonics_mag_2",
            "Harmonics_mag_3",
            "Harmonics_mag_4",
            "Harmonics_mag_5",
            "Harmonics_mag_6",
            "Harmonics_mag_7",
            "Harmonics_mse",
            "Harmonics_phase_2",
            "Harmonics_phase_3",
            "Harmonics_phase_4",
            "Harmonics_phase_5",
            "Harmonics_phase_6",
            "Harmonics_phase_7",
            "IAR_phi",
            "iqr",
            "last_diffmaglim_before_fid",
            "last_mjd_before_fid",
            "LinearTrend",
            "max_diffmaglim_after_fid",
            "max_diffmaglim_before_fid",
            "MaxSlope",
            "Mean",
            "mean_mag",
            "Meanvariance",
            "MedianAbsDev",
            "MedianBRP",
            "median_diffmaglim_after_fid",
            "median_diffmaglim_before_fid",
            "MHPS_high"
        ],
        "stamps": true
    },
    "oids": [
        "ZTF18abzavvs",
        "ZTF19aabetsw",
        "ZTF18abuhshf",
        "ZTF18abnokhg",
        "ZTF19abljelm",
        "ZTF18acmwkou",
        "ZTF19aakpvqh",
        "ZTF18abtmkxz",
        "ZTF18abihaed",
        "ZTF20acuzxjj",
        "ZTF18actxasz",
        "ZTF19acgkjiw",
        "ZTF20aagralz",
        "ZTF19acbvgol",
        "ZTF19acehyfz",
        "ZTF20acywitq",
        "ZTF19abojumh"
    ]
}
```


#### Get feature names

```http
  GET /versioner/features
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `-` | `-` | - |

#### Body

```json

```

#### Response

```json
  {
    "features": [
        "Amplitude",
        "AndersonDarling",
        "Autocor_length",
        "Beyond1Std",
        "Con",
        "delta_mag_fid",
        "delta_mjd_fid",
        "delta_period",
        "dmag_first_det_fid",
        "dmag_non_det_fid",
        "Eta_e",
        "ExcessVar",
        "first_mag",
        "gal_b",
        "gal_l",
        "GP_DRW_sigma",
        "GP_DRW_tau",
        "g-r_max",
        "g-r_max_corr",
        "g-r_mean",
        "g-r_mean_corr",
        "Gskew",
        "g-W2",
        "g-W3",
        "Harmonics_mag_1",
        "Harmonics_mag_2",
        "Harmonics_mag_3",
        "Harmonics_mag_4",
        "Harmonics_mag_5",
        "Harmonics_mag_6",
        "Harmonics_mag_7",
        "Harmonics_mse",
        "Harmonics_phase_2",
        "Harmonics_phase_3",
        "Harmonics_phase_4",
        "Harmonics_phase_5",
        "Harmonics_phase_6",
        "Harmonics_phase_7",
        "IAR_phi",
        "iqr",
        "last_diffmaglim_before_fid",
        "last_mjd_before_fid",
        "LinearTrend",
        "max_diffmaglim_after_fid",
        "max_diffmaglim_before_fid",
        "MaxSlope",
        "Mean",
        "mean_mag",
        "Meanvariance",
        "MedianAbsDev",
        "MedianBRP",
        "median_diffmaglim_after_fid",
        "median_diffmaglim_before_fid",
        "MHPS_high",
        "MHPS_low",
        "MHPS_non_zero",
        "MHPS_PN_flag",
        "MHPS_ratio",
        "min_mag",
        "Multiband_period",
        "n_det",
        "n_neg",
        "n_non_det_after_fid",
        "n_non_det_before_fid",
        "n_pos",
        "PairSlopeTrend",
        "PercentAmplitude",
        "Period_band",
        "positive_fraction",
        "Power_rate_1/2",
        "Power_rate_1/3",
        "Power_rate_1/4",
        "Power_rate_2",
        "Power_rate_3",
        "Power_rate_4",
        "PPE",
        "Psi_CS",
        "Psi_eta",
        "Pvar",
        "Q31",
        "rb",
        "Rcs",
        "r-W2",
        "r-W3",
        "SF_ML_amplitude",
        "SF_ML_gamma",
        "sgscore1",
        "Skew",
        "SmallKurtosis",
        "SPM_A",
        "SPM_beta",
        "SPM_chi",
        "SPM_gamma",
        "SPM_t0",
        "SPM_tau_fall",
        "SPM_tau_rise",
        "Std",
        "StetsonK",
        "W1-W2",
        "W2-W3"
    ]
}
```

#### Download dataset 

```http
  GET /versioner/dataset/{did}/version/{version}/download
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `did`      | `integer` | **Required**. dataset index |
| `version`      | `integer` | **Required**. version number |

#### Body

```json

```

#### Response

.csv File with all dataset information


#### Post new dataset

```http
  POST /versioner/dataset/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `-` | `-` | - |

#### Body

```json
  {
    "name": "Dataset to test update4",
    "author": "asanchez2017",
    "description": "test test test",
    "oids": [
        "ZTF18abzavvs",
        "ZTF19aabetsw"
    ],
    "specs": {
        "features": [
            "gal_l",
            "GP_DRW_sigma",
            "GP_DRW_tau",
            "g-r_max",
            "g-r_max_corr",
            "g-r_mean",
            "g-r_mean_corr",
            "Gskew",
            "g-W2",
            "g-W3",
            "Harmonics_mag_1",
            "Harmonics_mag_2",
            "Harmonics_mag_3",
            "Harmonics_mag_4",
            "Harmonics_mag_5",
            "Harmonics_mag_6",
            "Harmonics_mag_7",
            "Harmonics_mse",
            "Harmonics_phase_2",
            "Harmonics_phase_3",
            "Harmonics_phase_4",
            "Harmonics_phase_5",
            "Harmonics_phase_6",
            "Harmonics_phase_7",
            "IAR_phi",
            "iqr",
            "last_diffmaglim_before_fid",
            "last_mjd_before_fid",
            "LinearTrend",
            "max_diffmaglim_after_fid",
            "max_diffmaglim_before_fid",
            "MaxSlope",
            "Mean",
            "mean_mag",
            "Meanvariance",
            "MedianAbsDev",
            "MedianBRP",
            "median_diffmaglim_after_fid",
            "median_diffmaglim_before_fid",
            "MHPS_high"
        ],
        "stamps": true
    },
    "parent_did": 1
  }

```

#### Response

```json
  {
    "success": true,
    "message": "Dataset created successfully.",
    "dataset": {
        "did": 20,
        "name": "Dataset to test update5",
        "version": 1,
        "author": "asanchez2017"
    }
  }
```


#### Update new dataset

```http
  UPDATE /versioner/dataset/{did}/update
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `did`      | `integer` | **Required**. dataset index |

#### Body

```json
  {
    "name": "esto fue agregado en una update",
    "description": "trololololol",
    "specs": {
        "features": [
            "gal_l",
            "GP_DRW_sigma",
            "g-r_mean",
            "g-r_mean_corr",
            "Harmonics_mag_2",
            "Harmonics_mag_3"
        ],
        "stamps": true
    },
    "oids_add": [ 
    ],
    "oids_delete": [
    ],
    "collaborator": "asanchez2017"
  } 
```

#### Response

```json
  {
    "success": true,
    "message": "name updated,description updated,specs updated,",
    "updated_dataset": {
        "did": 16,
        "name": "esto fue agregado en una update 21322",
        "description": "trololololol",
        "old_version": 1,
        "new_version": 2,
        "specs": {
            "det": false,
            "non_det": false,
            "lc": false,
            "xmatch": false,
            "features": [
                "gal_l",
                "GP_DRW_sigma",
                "g-r_mean",
                "g-r_mean_corr",
                "Harmonics_mag_2",
                "Harmonics_mag_3"
            ],
            "stamps": true
        },
        "added_oids": [],
        "deleted_oids": []
    }
}
```
