import React, { useState } from 'react';

import CMSLink from 'components/CMSLinkify';

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

  return (
    <div className={className}>
      <span>
        <CMSLink text={shownText} />
      </span>

      {isNeeded && (
        <button
          id={id}
          className="display--inline-block btn btn-link"
          onClick={() => setIsExpanded(!isExpanded)}
        >
          {isExpanded ? '...less' : 'more'}
        </button>
      )}
    </div>
  );
}
