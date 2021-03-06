import * as React from 'react';
import { connect } from 'react-redux';

import Pagination from 'react-js-pagination';
import { Modal } from 'react-bootstrap';

import { GlobalState } from 'ducks/rootReducer';
import { getDataAssets } from 'ducks/dataAssets/reducer';
import { GetDataAssetsRequest } from 'ducks/dataAssets/types';
import { DataAsset } from 'interfaces';

import InfoButton from 'components/InfoButton';
import CMSShowMoreText from 'components/CMSShowMoreText';
import ExpandText from './ExpandText';
import CMSLink from 'components/CMSLinkify';
// import ShimmeringResourceLoader from '../ShimmeringResourceLoader';

import {
  DATA_ASSETS_LABEL,
  DATA_ASSETS_INFO_TEXT,
  DATA_ASSETS_PER_PAGE,
  DATA_ASSETS_HELP_TEXT,
} from './constants';

import './styles.scss';
import { bindActionCreators } from 'redux';

interface DataAssetsState {
  activePage: number;
}

export interface PropsFromState {
  isLoading: boolean;
  dataAssets: DataAsset[];
}

interface DispatchFromProps {
  getDataAssets: () => GetDataAssetsRequest
}

type DataAssetProps = PropsFromState & DispatchFromProps

export class DataAssets extends React.Component<DataAssetProps, DataAssetsState> {
  constructor(props) {
    super(props);

    this.state = {
      activePage: 1,
    };
  }

  componentDidMount() {
    this.props.getDataAssets()
  }

  handlePageChange(pageNumber) {
    this.setState({ activePage: pageNumber });
  }


  render() {
    // let content = (
    //   <ShimmeringResourceLoader numItems={DATA_ASSETS_PER_PAGE} />
    // );

    const startIndex = (this.state.activePage - 1) * DATA_ASSETS_PER_PAGE;
    const content = (
      <div className="row">
        <div className="col-sm-12">
          <div className="row">
            {this.props.dataAssets.slice(
              startIndex,
              startIndex + DATA_ASSETS_PER_PAGE
            ).map((asset, index) => (
              <div className="col-sm-4" key={index}>
                <h3>
                  <a
                    id={`dataasset-anchor-${asset.schema.toLowerCase()}`}
                    className=""
                    href={`/search?resource=table&index=0&filters=%7B"schema"%3A"${asset.schema.toLowerCase()}"%7D`}
                  >
                    {asset.schema_title}
                  </a>
                </h3>
                <ExpandText key={index} title={asset.schema_title} text={asset.schema_description} id={`data-asset-${asset.schema}`} />
              </div>
            ))}
            <div className="col-sm-4" style={{background:'#F0F1F1'}}>
              <h3 id='call-out-header' tabIndex={0}style={{color:'black'}}>{DATA_ASSETS_HELP_TEXT.title}</h3>
              <p id='call-out-textfield' tabIndex={0}>
                <CMSLink text={DATA_ASSETS_HELP_TEXT.description} />
              </p>
            </div>
          </div>
          <div className="row">
            <div className="col-sm-12">
              <Pagination
                activePage={this.state.activePage}
                itemsCountPerPage={DATA_ASSETS_PER_PAGE}
                totalItemsCount={this.props.dataAssets.length}
                pageRangeDisplayed={5}
                onChange={this.handlePageChange.bind(this)}
              />
            </div>
          </div>
          <div className="row view-all">
            <div style={{ display: "flex", justifyContent: "flex-end" }}>
              <a
                id="data-assets-anchor-view-all"
                href='/data_assets'
                style={{ color: "#0071bc", textDecoration: "underline", fontWeight: "bold" }}>
                View all Data Assets
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  height="24"
                  viewBox="0 0 24 15"
                  width="24"
                  style={{ marginLeft: "0.5rem" }}
                >
                  <path d="M0 0h24v24H0z" fill="none" />
                  <path
                    d="M12 4l-1.41 1.41L16.17 11H4v2h12.17l-5.58 5.59L12 20l8-8z"
                    fill='#0071bc'
                  />
                </svg>
              </a>
            </div>
          </div>
        </div>
      </div>
    );

    return (
      <article id="dataasset-popular-list" className="popular-data-asset-list">
        <div><hr /></div>
        <div id="dataasset-popular-list-header" className="popular-data-assets-header">
          <h2 id="dataasset-popular-list-header-label" className="popular-data-assets-header-text" tabIndex={0}>
            {DATA_ASSETS_LABEL}
          </h2>
          <InfoButton infoText={DATA_ASSETS_INFO_TEXT} />
        </div>

        {content}
      </article>
    );
  }
}

export const mapStateToProps = ({ dataAssets }: GlobalState) => ({
  isLoading: dataAssets.dataAssetsIsLoaded,
  dataAssets: dataAssets.dataAssets
})

export const mapDispatchToProps = (dispatch: any) =>
  bindActionCreators({ getDataAssets }, dispatch);

export default connect<PropsFromState, DispatchFromProps>(
  mapStateToProps,
  mapDispatchToProps
)(DataAssets)