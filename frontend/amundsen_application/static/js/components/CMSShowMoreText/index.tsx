import React, { useState } from 'react';

import CMSLink from 'components/CMSLinkify';
import '../../GlobalStyles/hide-element.css'
import { SHOW_MORE_TEXT, SHOW_LESS_TEXT } from '../../constants'

type CMSShowMoreTextProps = {
  text: string;
  limit?: number;
  className?: string;
  id?: string;
};

export default function CMSShowMoreText({
  id,
  text,
  className,
  limit = 250,
}: CMSShowMoreTextProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!text) {
    return null;
  }

  const isNeeded = text.length >= limit;
  const ellipsis = isNeeded ? '...' : '';
  const shownText =
    !isNeeded || isExpanded ? text : `${text.substring(0, limit)}${ellipsis}`;

  let verbiage = ''
  if (id?.includes('domain')) {
    console.log(id)
     verbiage = id?.replace(/-/g, ' ').split(" ").slice(1).join(" ");
  }

  return (
    <div className={className}>
      <span id={`${id}-textfield`} tabIndex={0}>
        <CMSLink text={shownText} />
      </span>

      {isNeeded && (
        <button
          id={`${id}-show-more-less-button`}
          className="display--inline-block btn btn-link"
          onClick={() => setIsExpanded(!isExpanded)}
        >
          {isExpanded ? SHOW_LESS_TEXT : SHOW_MORE_TEXT}
          <span className='hide-element'>{` toggle button for ${verbiage} domain`}</span>
        </button>
      )}
    </div>
  );
}
