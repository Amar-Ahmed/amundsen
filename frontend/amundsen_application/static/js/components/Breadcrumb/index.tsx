// Copyright Contributors to the Amundsen project.
// SPDX-License-Identifier: Apache-2.0

import * as React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';

import { DATASET_ALT_TXT } from './constants';

import './styles.scss';
import { loadPreviousSearch } from 'ducks/search/reducer';
import { LoadPreviousSearchRequest } from 'ducks/search/types';

export interface OwnProps {
  direction?: BreadcrumbDirection;
  path?: string;
  text?: string;
}

export interface MapDispatchToProps {
  loadPreviousSearch: () => LoadPreviousSearchRequest;
}

type BreadcrumbDirection = 'left' | 'right';

export type BreadcrumbProps = OwnProps & MapDispatchToProps;

export const Breadcrumb: React.FC<BreadcrumbProps> = (
  props: BreadcrumbProps
) => {
  const { direction = 'left', path, text } = props;
  if (path !== undefined && text !== undefined) {
    return (
      <div className="amundsen-breadcrumb">
        <Link to={path} id='amundsen-breadcrumb-link' className="btn btn-flat-icon title-3">
          {direction === 'left' && (
            <img id='amundsen-breadcrumb-link-image' className="icon icon-left" alt={DATASET_ALT_TXT} />
          )}
          <span id={`breadcrumb-span-${text}`}>{text}</span>
          {direction === 'right' && <img className="icon icon-right" alt="" />}
        </Link>
      </div>
    );
  }
  return (
    <div className="amundsen-breadcrumb">
      {/* eslint-disable jsx-a11y/anchor-is-valid */}
      <a
        id='amundsen-breadcrumb-anchor'
        onClick={props.loadPreviousSearch}
        className="btn btn-flat-icon title-3"
      >
        {direction === 'left' && (
          <img id='amundsen-breadcrumb-anchor-image' className="icon icon-left" alt={DATASET_ALT_TXT} />
        )}
        {direction === 'right' && <img className="icon icon-right" alt="" />}
      </a>
    </div>
  );
};

export const mapDispatchToProps = (dispatch: any) =>
  bindActionCreators({ loadPreviousSearch }, dispatch);

export default connect<{}, MapDispatchToProps>(
  null,
  mapDispatchToProps
)(Breadcrumb);
