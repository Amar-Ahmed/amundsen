import React, { useState } from 'react';

type TruncateTextProps = {
  text: string;
  limit?: number;
  className?: string;
};

export default function TruncateText({
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
      <span>
        {shownText}
      </span>

      {isNeeded && (
        <button
          className="display--inline-block btn btn-link"
          onClick={() => setIsExpanded(!isExpanded)}
        >
          {isExpanded ? '...less' : 'more'}
        </button>
      )}
    </div>
  );
}
