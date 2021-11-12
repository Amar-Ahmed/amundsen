import { SagaIterator } from "redux-saga";
import { call, put, takeEvery } from "redux-saga/effects";

import * as API from "./api/v0";
import { getDataAssetsFailure, getDataAssetsSuccess } from "./reducer";
import { GetDataAssets } from "./types";

export function* getDataAssetsWorker(): SagaIterator {
  try {
    const dataAssets = yield call(API.getDataAssets);
    yield put(getDataAssetsSuccess(dataAssets));
  } catch (e) {
    yield put(getDataAssetsFailure());
  }
}

export function* getDataAssetsWatcher(): SagaIterator {
  yield takeEvery(GetDataAssets.REQUEST, getDataAssetsWorker);
}
