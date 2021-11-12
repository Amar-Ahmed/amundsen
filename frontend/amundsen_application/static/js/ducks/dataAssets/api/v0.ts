import axios, { AxiosResponse } from 'axios'

import { DataAsset } from 'interfaces'

export type DataAssetsAPI = {
    msg: string;
    schemas: DataAsset[]
}

export function getDataAssets() {
    return axios
        .get('/api/metadata/v0/schemas')
        .then((resp: AxiosResponse<DataAssetsAPI>) => {
            console.log("[ducks/dataAssets/api] /SCHEMAS:", resp)
            return resp
        })
        .then((resp: AxiosResponse<DataAssetsAPI>) => resp.data.schemas)
}