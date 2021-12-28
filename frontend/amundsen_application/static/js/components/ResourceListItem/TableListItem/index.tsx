// Copyright Contributors to the Amundsen project.
// SPDX-License-Identifier: Apache-2.0

import * as React from 'react';
import { Link } from 'react-router-dom';

import { ResourceType, TableResource } from 'interfaces';

// import BookmarkIcon from 'components/Bookmark/BookmarkIcon';

import { getSourceDisplayName, getSourceIconClass } from 'config/config-utils';

import BadgeList from 'features/BadgeList';
import SchemaInfo from 'components/ResourceListItem/SchemaInfo';
import { LoggingParams } from '../types';

import './table-style.css'

export interface TableListItemProps {
  table: TableResource;
  logging: LoggingParams;
}

class TableListItem extends React.Component<TableListItemProps, {}> {
  getLink = () => {
    const { table, logging } = this.props;

    return (
      `/table_detail/${table.cluster}/${table.database}/${table.schema}/${table.name}` +
      `?index=${logging.index}&source=${logging.source}`
    );
  };

  generateResourceIconClass = (
    databaseId: string,
    resource: ResourceType
  ): string => `icon resource-icon ${getSourceIconClass(databaseId, resource)}`;

  render() {
    const { table } = this.props;

    return (
      <li className="list-group-item clickable">
        <Link
          id={`${table.name}-anchor`}
          className="resource-list-item table-list-item"
          to={this.getLink()}
        >
          <div className="resource-info">
            <span
              id={`${table.name}-icon`}
              className={this.generateResourceIconClass(
                table.database,
                table.type
              )}
            />
            <div className="resource-info-text my-auto">
              <div className="resource-name title-2">
                <div id={`${table.schema}-${table.name}-text`} className="truncated">
                  {table.schema_description && (
                    <SchemaInfo
                      schema={table.schema}
                      table={table.name}
                      desc={table.schema_description}
                    />
                  )}
                  {!table.schema_description && `${table.schema}.${table.name}`}
                </div>
                {/* <BookmarkIcon
                  bookmarkKey={table.key}
                  resourceType={table.type}
                /> */}
              </div>
              <div id={`${table.name.replace(/\s+/, '-')}-description`} className="body-secondary-3 truncated">
                {table.description}
              </div>
            </div>
          </div>
        </Link>
      </li>
    );
  }
}

export default TableListItem;
