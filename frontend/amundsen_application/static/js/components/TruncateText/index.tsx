import React, { useState } from 'react';
import '../../GlobalStyles/hide-element.css'

type TruncateTextProps = {
  id?: string;
  text: string;
  limit?: number;
  className?: string;
};

export default function TruncateText({
  id,
  text,
  className,
  limit = 200,
}: TruncateTextProps) {
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
      <span id={`${id}-textfield`} tabIndex={0}>
        {shownText}
      </span>

      {isNeeded && (
        <button
          id={`${id}-show-more-less-button`}
          className="display--inline-block btn btn-link"
          onClick={() => setIsExpanded(!isExpanded)}
        >
          {isExpanded ? '...less' : 'more'}
          <span className='hide-element'>{`${id}-show-more-less-toggle`}</span>
        </button>
      )}
    </div>
  );
}
