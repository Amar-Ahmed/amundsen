// Copyright Contributors to the Amundsen project.
// SPDX-License-Identifier: Apache-2.0

import React, { Component } from 'react';
import { Tab, Tabs, Table } from 'react-bootstrap';
import { RouteComponentProps } from 'react-router';
import Breadcrumb from 'components/Breadcrumb';
import Truncate from '../../components/TruncateText';
import { getDomains } from '../../ducks/domains/api/v0';
import './style.css';

export class DomainsPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      domains: [],
    };
  }
  componentDidMount() {
    getDomains()
      .then((response) => this.setState({ domains: response }))
      .catch((err) => console.log(err));
  }

  renderDomainList = () => {
    return this.state.domains.map((domain) => {
      if (domain.domain_data_asset) {
        return (
          <tr>
            <td className="title-3">
              <a
                id={`domain-anchor-${domain.domain_name.replace(/\s+/, '-')}`}
                className="capitalize"
                href={`/domains/${domain.domain_name}/`}
              >
                {domain.domain_name}
              </a>
            </td>
            <td className="domains-list-description-container">
              <Truncate id={domain.domain_name.replace(/\s+/, '-')} text={domain.domain_description} role='domain'/>
            </td>
          </tr>
        );
      } else {
        return (
          <tr>
            <td className="title-3">
              <span className="capitalize" tabIndex={0}>{domain.domain_name}</span>
            </td>
            <td className="domains-list-description-container">
              <Truncate id={domain.domain_name.replace(/\s+/, '-')} text={domain.domain_description} />
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
                  <span className="current-link"> Domains</span>
                </div>
              </div>
              <div className="row" style={{ marginTop: '36px' }}>
                <h2 tabIndex={0}>{'Domains'}</h2>
              </div>
              <div className="row " style={{ marginTop: '24px' }}>
                <p className="subtitle-3" tabIndex={0}>
                  A domain is a body of knowledge in a specific area that
                  provides context for data meaning and usage. It reflects how
                  data consumers and contributors think and talk about their
                  data. Domains provide an organizing structure for information
                  about the data described in the Enterprise User Data Catalog.
                  It promotes understanding by providing a business context for
                  data assets and potentially the relationships between assets.
                </p>
              </div>
              <div className="row " style={{ marginTop: '24px' }}>
                <Table responsive>
                  <thead>
                    <tr>
                      <th className="title-3" style={{ minWidth: '170px' }} tabIndex={0}>
                      <h4>Name</h4>
                      </th>
                      <th className="title-3" style={{ maxWidth: '170px' }} tabIndex={0}>
                        <h4>Description</h4>
                      </th>
                    </tr>
                  </thead>
                  <tbody>{this.renderDomainList()}</tbody>
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

export default DomainsPage;
function activeTabTitle(activeTabTitle) {
  throw new Error('Function not implemented.');
}
