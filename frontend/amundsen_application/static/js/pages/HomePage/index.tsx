// Copyright Contributors to the Amundsen project.
// SPDX-License-Identifier: Apache-2.0

import * as React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { RouteComponentProps } from 'react-router';

import { resetSearchState } from 'ducks/search/reducer';
import { UpdateSearchStateReset } from 'ducks/search/types';

// import MyBookmarks from 'components/Bookmark/MyBookmarks';
import Breadcrumb from 'components/Breadcrumb';
// import PopularTables from 'components/PopularTables';
import SearchBar from 'components/SearchBar';
import TagsListContainer from 'components/Tags';
import Announcements from 'components/Announcements';

import CMSIntro from 'components/CMSIntro';
import DataAssets from 'components/CMSDataAssetCard';
import DomainCard from 'components/CMSDomainCard';

import { announcementsEnabled } from 'config/config-utils';

import { SEARCH_BREADCRUMB_TEXT, HOMEPAGE_TITLE } from './constants';

import './styles.scss';

export interface DispatchFromProps {
  searchReset: () => UpdateSearchStateReset;
}

export type HomePageProps = DispatchFromProps & RouteComponentProps<any>;

export class HomePage extends React.Component<HomePageProps> {
  componentDidMount() {
    this.props.searchReset();
  }

  render() {
    /* TODO, just display either popular or curated tags,
    do we want the title to change based on which
    implementation is being used? probably not */
    return (
      <main id="home-main" className="container home-page">
        <div id="home-inner-container" className="row">
          <div
          id="home-content"
            className={`col-xs-12 ${
              announcementsEnabled() ? 'col-md-8' : 'col-md-offset-1 col-md-10'
            }`}
          >
            <h1 id="home-title" className="sr-only">{HOMEPAGE_TITLE}</h1>

            {/* <div>
              <CMSIntro />
            </div> */}

            <div id="home-navbar" className="home-element-container-half-height">
              <SearchBar />
              <div id="home-navbar-breadcrumb" className="filter-breadcrumb pull-right">
                <Breadcrumb
                  direction="right"
                  path="/search"
                  text={SEARCH_BREADCRUMB_TEXT}
                />
              </div>
            </div>
            <div id="home-domains" className="home-element-container">
              <DomainCard/>
            </div>
            <div id="home-dataassets" className="home-element-container">
              <DataAssets />
            </div>

            <div id="home-tags" className="home-element-container">
              <TagsListContainer shortTagsList />
            </div>
            {/* <div className="home-element-container">
              <MyBookmarks />
            </div> */}
            {/* <div className="home-element-container">
              <PopularTables />
            </div> */}
          </div>
          {announcementsEnabled() && (
            <div id="home-announcements" className="col-xs-12 col-md-offset-1 col-md-3">
              <Announcements />
            </div>
          )}
        </div>
      </main>
    );
  }
}

export const mapDispatchToProps = (dispatch: any) =>
  bindActionCreators(
    {
      searchReset: () => resetSearchState(),
    },
    dispatch
  );

export default connect<DispatchFromProps>(null, mapDispatchToProps)(HomePage);
