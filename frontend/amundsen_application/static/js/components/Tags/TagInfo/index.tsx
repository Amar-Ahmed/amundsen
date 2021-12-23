// Copyright Contributors to the Amundsen project.
// SPDX-License-Identifier: Apache-2.0

import * as React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { ResourceType, Tag, SearchType } from 'interfaces';

import { updateSearchState } from 'ducks/search/reducer';
import { UpdateSearchStateRequest } from 'ducks/search/types';
import { logClick } from 'ducks/utilMethods';

import './styles.scss';

import './tag-info.css'

interface OwnProps {
  data: Tag;
  compact?: boolean;
}

export interface DispatchFromProps {
  searchTag: (tagName: string) => UpdateSearchStateRequest;
}

export type TagInfoProps = OwnProps & DispatchFromProps;

export class TagInfo extends React.Component<TagInfoProps> {
  static defaultProps = {
    compact: true,
  };

  onClick = (e) => {
    const name = this.props.data.tag_name;
    logClick(e, {
      target_type: 'tag',
      label: name,
    });
    this.props.searchTag(name);
  };

  render() {
    const name = this.props.data.tag_name;

    return (
      <button
        id={`tag::${name}`}
        className={'btn tag-button' + (this.props.compact ? ' compact' : '')}
        onClick={this.onClick}
      >
        <span id={`tag-name-${name.replace(/\s+/, '-')}`} className="tag-name" aria-hidden="true" aria-label={name}>{name}</span>
        {this.props.compact && <><span className="hide-element">Tag: {name}</span></>}
        {!this.props.compact && (
          <>
          <span id={`tag-count-${name.replace(/\s+/, '-')}`} className="tag-count" aria-hidden="true">{this.props.data.tag_count}</span>
          <span className="hide-element">{this.props.data.tag_count} instance of tag {name}</span>
          </>
        )}
      </button>
    );
  }
}

export const mapDispatchToProps = (dispatch: any) =>
  bindActionCreators(
    {
      searchTag: (tagName: string) =>
        updateSearchState({
          filters: {
            [ResourceType.dashboard]: { tag: tagName },
            [ResourceType.table]: { tag: tagName },
          },
          submitSearch: true,
        }),
    },
    dispatch
  );

export default connect<null, DispatchFromProps, OwnProps>(
  null,
  mapDispatchToProps
)(TagInfo);
