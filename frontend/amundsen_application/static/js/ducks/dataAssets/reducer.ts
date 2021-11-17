import { DataAsset } from "interfaces";

import {
  GetDataAssets,
  GetDataAssetsRequest,
  GetDataAssetsResponse,
} from "./types";

/* ACTIONS */
export function getDataAssets(): GetDataAssetsRequest {
  return { type: GetDataAssets.REQUEST };
}

export function getDataAssetsFailure(): GetDataAssetsResponse {
  return {
    type: GetDataAssets.FAILURE,
    payload: { schemas: [] },
  };
}

export function getDataAssetsSuccess(
  schemas: DataAsset[]
): GetDataAssetsResponse {
  return {
    type: GetDataAssets.SUCCESS,
    payload: { schemas },
  };
}

/* REDUCER */
export interface DataAssetsReducerState {
  dataAssets: DataAsset[];
  dataAssetsIsLoaded: boolean;
}

const initialState: DataAssetsReducerState = {
  dataAssets: [],
  dataAssetsIsLoaded: false,
};

export default function reducer(
  state: DataAssetsReducerState = initialState,
  action
): DataAssetsReducerState {
  switch (action.type) {
    case GetDataAssets.REQUEST:
      return { ...state, ...initialState };
    case GetDataAssets.SUCCESS:
    case GetDataAssets.FAILURE:
      return {
        ...state,
        dataAssets: (<GetDataAssetsResponse>action).payload.schemas,
        dataAssetsIsLoaded: true,
      };
    default:
      return state;
  }
}
