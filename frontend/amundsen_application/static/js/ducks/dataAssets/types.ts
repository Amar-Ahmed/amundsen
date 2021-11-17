import { DataAsset } from "interfaces";

export enum GetDataAssets {
    REQUEST = 'amundsen/dataAssets/GET_DATA_ASSETS_REQUEST',
    SUCCESS = 'amundsen/dataAssets/GET_DATA_ASSETS_SUCCESS',
    FAILURE = 'amundsen/dataAssets/GET_DATA_ASSETS_FAILURE',
}

export interface GetDataAssetsRequest {
    type: GetDataAssets.REQUEST
}

export interface GetDataAssetsResponse {
    type: GetDataAssets.SUCCESS | GetDataAssets.FAILURE,
    payload: {
        schemas: DataAsset[]
    }
}