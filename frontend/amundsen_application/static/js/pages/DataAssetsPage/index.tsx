// Copyright Contributors to the Amundsen project.
// SPDX-License-Identifier: Apache-2.0

import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Tab, Tabs, Table } from 'react-bootstrap';
import { RouteComponentProps } from 'react-router';
import Breadcrumb from 'components/Breadcrumb';
import Truncate from '../../components/TruncateText';
import { GlobalState } from 'ducks/rootReducer';
import { getDataAssets } from 'ducks/dataAssets/reducer';
import { GetDataAssetsRequest } from 'ducks/dataAssets/types';
import { DataAsset } from 'interfaces';
import { bindActionCreators } from 'redux';
import './style.css';

export interface PropsFromState {
  isLoading: boolean;
  dataAssets: DataAsset[];
}

interface DispatchFromProps {
  getDataAssets: () => GetDataAssetsRequest
}

type DataAssetProps = PropsFromState & DispatchFromProps


export class DataAssetsPage extends React.Component<DataAssetProps> {
  constructor(props) {
    super(props);
    this.state = {
      dataAssets: [],
    };
  }
  componentDidMount() {
    this.props.getDataAssets()
  }

  renderDataAssetList = () => {
    return this.props.dataAssets.map((asset, index) => {
      if (asset) {
        return (
          <tr key={index}>
            <td className="title-3">
              <a
                id={`dataasset-anchor-${asset.schema.toLowerCase()}`}
                href={`/search?resource=table&index=0&filters=%7B"schema"%3A"${asset.schema.toLowerCase()}"%7D`}
              >
                {asset.schema_title}
              </a>
            </td>
            <td className="data-asset-list-description-container">
              <Truncate id={`${asset.schema.replace(/\s+/, '-')}-description`} text={asset.schema_description} />
            </td>
          </tr>
        );
      } else {
        return (
          <tr>
            <td className="title-3">
              <span className="capitalize">{'.'}</span>
            </td>
            <td className="data-asset-list-description-container">
              <Truncate text={'.'} />
            </td>
          </tr>
        );
      }
    });
  };

  render() {
    return (
      <>
        <main className="container">
          <div className="row">
            <div className="col-xs-12 col-md-10 col-md-offset-1">
              <div className="row" style={{ marginTop: '24px' }}>
                <div className="amundsen-breadcrumb">
                  <Breadcrumb direction="right" path="/" text="Home" />
                  <span className="current-link"> Data Assets</span>
                </div>
              </div>
              <div className="row" style={{ marginTop: '36px' }}>
                <h2 id='data-asset-header' tabIndex={0}>{'Data Assets'}</h2>
              </div>
              <div className="row " style={{ marginTop: '24px' }}>
                <p id='data-asset-text' className="subtitle-3" tabIndex={0}>
                  A data asset is a data set or group of data sets that carry relevant data pertaining to an organization’s initiatives. The Enterprise User Data Catalog promotes understanding of data available within a data asset as well as potential relationships with other data assets by displaying details such as table names and descriptions, column names and descriptions, and data types.
                </p>
              </div>
              <div className="row " style={{ marginTop: '24px' }}>
                <Table responsive>
                  <thead>
                    <tr>
                      <th className="title-3" style={{ minWidth: '170px' }} tabIndex={0}>
                        <h4 id='data-asset-name-column'>Name</h4>
                      </th>
                      <th className="title-3" style={{ maxWidth: '170px' }} tabIndex={0}>
                        <h4 id='data-asset-description-column'>Description</h4>
                      </th>
                    </tr>
                  </thead>
                  <tbody>{this.renderDataAssetList()}</tbody>
                </Table>
              </div>
            </div>
          </div>
        </main>
      </>
    );
  }
}

export const TextContainer = ({ title, content }) => (
  <div
    className="row text-container"
    style={{ marginTop: '24px', marginLeft: '4px' }}
  >
    <h4 className="text-container-title">{title}</h4>
    <p>{content}</p>
  </div>
);

export const mapStateToProps = ({ dataAssets }: GlobalState) => ({
  isLoading: dataAssets.dataAssetsIsLoaded,
  dataAssets: dataAssets.dataAssets
})

export const mapDispatchToProps = (dispatch: any) =>
  bindActionCreators({ getDataAssets }, dispatch);

export default connect<PropsFromState, DispatchFromProps>(
  mapStateToProps,
  mapDispatchToProps
)(DataAssetsPage)
function activeTabTitle(activeTabTitle) {
  throw new Error('Function not implemented.');
}