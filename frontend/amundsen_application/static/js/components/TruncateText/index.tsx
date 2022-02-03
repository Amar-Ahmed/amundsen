import React, { useState } from 'react';
import '../../GlobalStyles/hide-element.css'
import { SHOW_MORE_TEXT, SHOW_LESS_TEXT } from '../../constants'

type TruncateTextProps = {
  id?: string;
  text: string;
  limit?: number;
  className?: string;
  role?: string;
};

export default function TruncateText({
  id,
  text,
  className,
  limit = 200,
  role,
}: TruncateTextProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!text) {
    return null;
  }

  const isNeeded = text.length >= limit;
  const ellipsis = isNeeded ? '...' : '';
  const shownText =
    !isNeeded || isExpanded ? text : `${text.substring(0, limit)}${ellipsis}`;
  
  let verbiage = ''
  
  if(role==='domain'){
    verbiage =id?.replace(/-/g, ' ')  +' domain'
  } else if(role==='data-asset'){
    verbiage = id?.replace(/-/g, ' ').split(" ").splice(0,1).join("").replace(/_/g, ' ').replace(/-/g, " ") +' data asset'
  }else{
    verbiage = id?.replace(/-/g, ' ').split(" ").splice(0,1).join(" ").replace(/_/g, ' ') +' data asset'
  }

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
          {isExpanded ? SHOW_LESS_TEXT : SHOW_MORE_TEXT}
          <span className='hide-element'>{` toggle button for ${verbiage}`}</span>
        </button>
      )}
    </div>
  );
}
