// Copyright Contributors to the Amundsen project.
// SPDX-License-Identifier: Apache-2.0

import * as React from 'react';

import './styles.scss';

import { ResourceType } from 'interfaces';
import {
  RESOURCE_HEADER_TITLE,
  SOURCE_HEADER_TITLE,
  BADGES_HEADER_TITLE,
  LAST_UPDATED_HEADER_TITLE,
} from './constants';

export interface ResourceListHeaderProps {
  resourceTypes: ResourceType[];
}

const contentHeaderTitle = (type: ResourceType): string => {
  switch (type) {
    case ResourceType.dashboard:
      return LAST_UPDATED_HEADER_TITLE;

    default:
      return BADGES_HEADER_TITLE;
  }
};
const ResourceListHeader: React.FC<ResourceListHeaderProps> = ({
  resourceTypes,
}: ResourceListHeaderProps) => {
  const contentHeader =
    resourceTypes.length === 1 ? contentHeaderTitle(resourceTypes[0]) : '';
  return (
    <div className="resource-list-header">
      <span className="resource">
        <span id="resource-header-title" className="resource-text">{RESOURCE_HEADER_TITLE}</span>
      </span>
    </div>
  );
};

export default ResourceListHeader;
