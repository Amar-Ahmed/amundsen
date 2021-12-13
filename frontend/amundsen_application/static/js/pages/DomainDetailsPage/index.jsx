// Copyright Contributors to the Amundsen project.
// SPDX-License-Identifier: Apache-2.0

import React, { Component } from 'react';
import { Tab, Tabs, Table } from 'react-bootstrap';
import { RouteComponentProps } from 'react-router';
import Breadcrumb from 'components/Breadcrumb';
import './style.css'
import { postDomains } from 'ducks/domains/api/v0';
import Truncate from '../../components/TruncateText';


// interface DomainProps extends RouteComponentProps<MatchParams>{
//   title: string;
// }

// interface MatchParams {
//   name: string;
// }

// interface DomainState {
//   activeTab: string;
// }
// export class DomainDetailsPage extends Component<DomainProps, DomainState> {
export class DomainDetailsPage extends Component {

  constructor(props) {
    super(props);
    this.state = {
      activeTab: 'updates',
      domainDetails: [],
    }
  }
  componentDidMount() {
    postDomains({ domain_name: this.props.match.params.name }).then(response =>
      this.setState({ domainDetails: response }))
      .catch(err => console.log(err))
  }
  updateState = (activeTabTitle) => {
    this.setState({ activeTab: activeTabTitle })
  }
  getDataAssetList = () => {
    if (this.state.domainDetails?.length > 0 && this.state.domainDetails[0].domain_data_asset?.length > 0) {
      return this.state.domainDetails[0].domain_data_asset.map(domain => {
        return (<tr>
          <td className='title-3'>
            <a href={`/search?resource=table&index=0&filters=%7B"schema"%3A"hive_${domain.schema.toLowerCase()}"%7D`}
              style={{ color: '#0071BC' }} >{domain.schema_title}
            </a></td>
          <td className='domains-list-description-container'>
            <Truncate text={domain.schema_description} />
          </td>
        </tr>)
      })
    }
  }

  render() {
    this.getDataAssetList()
    let descriptionContent = ''
    let updatesContent = ''
    if (this.state.domainDetails.length > 0) {
      descriptionContent = this.state.domainDetails[0].domain_description
      updatesContent = this.state.domainDetails[0].domain_updates
    } else {
      descriptionContent = ''
      updatesContent = ''
    }
    return (
      <>
        <main className="container">
          <div className="row">
            <div className="col-xs-12 col-md-10 col-md-offset-1">
              <div className="row" style={{ marginTop: '24px' }}>
                <div className="amundsen-breadcrumb">
                  <Breadcrumb
                    direction="right"
                    path="/"
                    text='Home'
                  />
                  <Breadcrumb
                    direction="right"
                    path="/domains"
                    text='Domains'
                  />
                  <span className='current-link capitalize'>{this.props.match.params.name}</span>
                </div>
              </div>
              <div className="row" style={{ marginTop: '36px' }}>
                <h2 className='capitalize'>{this.props.match.params.name}</h2>
              </div>
              <div className="row tab-container" style={{ marginTop: '24px' }}>
                <Tabs
                  defaultActiveKey="updates"
                  id="domain-id"
                  className="mb-3 domain-details-tab-container"
                  onSelect={(activeTabTitle) => this.updateState(activeTabTitle)}

                >
                  <Tab eventKey="updates" title="Updates" tabClassName={`${this.state.activeTab === 'updates' ? 'selected-tab' : ''}`}>
                    <TextContainer title={'Description'} content={descriptionContent} />
                    <TextContainer title={'Updates'} content={updatesContent} />
                    {/* <TextContainer title={'Contact'} content={''} /> */}
                  </Tab>
                  <Tab eventKey="data-asset" title="Data Assets" tabClassName={`${this.state.activeTab === 'data-asset' ? 'selected-tab' : ''}`}>
                    <TextContainer title={'Data Assets'} content={''} />
                    <Table responsive>
                      <thead>
                        <tr>
                          <th>Name</th>
                          <th>Data Asset Profile</th>
                        </tr>
                      </thead>
                      <tbody>
                        {/* {this.renderDataAssetList()} */}
                        {this.getDataAssetList()}
                        {/* <tr>
                        </tr> */}
                      </tbody>
                    </Table>
                  </Tab>
                </Tabs>
              </div>
            </div>
          </div>
        </main>
      </>
    );
  }
}

// type TextContainerProps = {
//   title: string,
//   content: string
// }

// export const TextContainer = ({ title, content }: TextContainerProps) => <div className="row text-container" style={{ marginTop: '24px', marginLeft: '4px' }}>
//   <h4 className='text-container-title'>{title}</h4>
//   <p>
//     {content}
//   </p>
// </div>

// export default DomainDetailsPage;
// function activeTabTitle(activeTabTitle: string) {
//   throw new Error('Function not implemented.');
// }
export const TextContainer = ({ title, content }) => <div className="row text-container" style={{ marginTop: '24px', marginLeft: '4px' }}>
  <h4 className='text-container-title'>{title}</h4>
  <p>
    {content}
  </p>
</div>

export default DomainDetailsPage;
function activeTabTitle(activeTabTitle) {
  throw new Error('Function not implemented.');
}

