// Copyright Contributors to the Amundsen project.
// SPDX-License-Identifier: Apache-2.0

import * as React from 'react';
import * as Avatar from 'react-avatar';
import { Link } from 'react-router-dom';

import { UserResource } from 'interfaces';
import { LoggingParams } from '../types';

export interface UserListItemProps {
  user: UserResource;
  logging: LoggingParams;
}

class UserListItem extends React.Component<UserListItemProps, {}> {
  getLink = () => {
    const { user, logging } = this.props;
    return `/user/${user.user_id}?index=${logging.index}&source=${logging.source}`;
  };

  renderUserInfo = (user: UserResource): JSX.Element[] | null => {
    const { role_name, team_name, user_id } = user;
    if (!role_name && !team_name) {
      return null;
    }

    const listItems: JSX.Element[] = [];
    if (role_name) {
      listItems.push(<li key={`${user_id}:role_name`}>{role_name}</li>);
    }
    if (team_name) {
      listItems.push(<li key={`${user_id}:team_name`}>{team_name}</li>);
    }
    return listItems;
  };

  render() {
    const { user } = this.props;
    const userInfo = this.renderUserInfo(user);
    return (
      <li className="list-group-item clickable">
        <Link className="resource-list-item user-list-item" to={this.getLink()}>
          <div className="resource-info">
            <Avatar name={user.display_name} size={24} round />
            <div className="resource-info-text my-auto">
              <div className="resource-name title-2">{user.display_name}</div>
              {userInfo && (
                <div className="body-secondary-3 truncated">
                  <ul>{userInfo}</ul>
                </div>
              )}
            </div>
          </div>
        </Link>
      </li>
    );
  }
}

export default UserListItem;
