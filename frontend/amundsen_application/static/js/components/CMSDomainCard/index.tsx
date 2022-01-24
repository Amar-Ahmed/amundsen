import * as React from 'react';

import CMSShowMoreText from 'components/CMSShowMoreText';
// import ShimmeringResourceLoader from '../ShimmeringResourceLoader';

import {
  DOMAINS,
  FEATURED_DOMAINS_LABEL,
  DOMAINS_PER_PAGE
} from './constants';

import './styles.scss';

import CMSLink from 'components/CMSLinkify';
import InfoButton from 'components/InfoButton';

interface DomainsState {
  activePage: number;
}

export default class CMSDomainCard extends React.Component<{}, DomainsState> {
  constructor(props) {
    super(props);

    this.state = {
      activePage: 1,
    };
  }

  componentDidMount() {
  }

  handlePageChange(pageNumber) {
    this.setState({ activePage: pageNumber });
  }

  render() {
    // let content = (
    //   <ShimmeringResourceLoader numItems={DATA_ASSETS_PER_PAGE} />
    // );

    const startIndex = (this.state.activePage - 1) * DOMAINS_PER_PAGE;
    const content = (
      <div className="row">
        <div className="col-sm-12">
          <div className="row">
            {DOMAINS.slice(
              startIndex,
              startIndex + DOMAINS_PER_PAGE
            ).map((domain, index) => (
              <div className="col-sm-4" key={index}>
                <h3 id={`domain-heading-${domain.title.replace(/\s+/, '-')}`} className='domain-heading'>
                  <a
                    id={`domain-heading-anchor-${domain.title}`}
                    className=""
                    href={`/domains${domain.path}`}
                  >
                    {domain.title}
                  </a>
                </h3>

                <CMSShowMoreText id={`domain-${domain.title.replace(/\s+/, '-')}`} text={domain.description} />
              </div>
            ))}
          </div>
          <br />
          <div className="row view-all">
            <div style={{display: "flex", justifyContent: "flex-end"}}>
              <a 
                id="domains-anchor-view-all" 
                href='/domains'
                style={{ color: "#0071bc", textDecoration: "underline", fontWeight: "bold"}}>
                View all Domains
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
      <article className="popular-data-asset-list">
        <div><hr /></div>
        <div className="popular-data-assets-header">
          <h2 id='homepage-domain-title' className="popular-data-assets-header-text" tabIndex={0}>
            {FEATURED_DOMAINS_LABEL}
          </h2>
        </div>
        {content}
      </article>
    );
  }
}
