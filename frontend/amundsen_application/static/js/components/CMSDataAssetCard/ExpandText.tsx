import React, { useState } from 'react';
import { Modal } from 'react-bootstrap';

import CMSLink from 'components/CMSLinkify';
import '../../GlobalStyles/hide-element.css'

type CMSShowMoreTextProps = {
  title: string;
  text: string;
  limit?: number;
  className?: string;
  id?: string;
};

export default function ExpandText({
  title,
  text,
  id,
  className,
  limit = 250,
}: CMSShowMoreTextProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!text) {
    return null;
  }

  const isNeeded = text.length >= limit;
  const ellipsis = isNeeded ? '...' : '';
  const shownText = `${text.substring(0, limit)}${ellipsis}`;

  let verbiage = ''
  if (id?.includes('data-asset')) {
     verbiage = id.replace(/-/g, ' ').replace(/_/g, ' ').split(" ").slice(2).join(" ");
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
          onClick={() => setIsExpanded(true)}
        >
          {'more'}
          <span className='hide-element'>{` toggle button for ${verbiage} data asset`}</span>
        </button>
      )}
      <DataAssetModal
        show={isExpanded}
        onHide={() => setIsExpanded(false)}
        title={title}
        description={text}
      />
    </div>
  );
}

function DataAssetModal(props) {
  return (
    <Modal
      {...props}
      size="xl"
      centered
    >
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter" className='modal-title'>
          {props.title}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <CMSLink text={props.description} />
      </Modal.Body>
    </Modal>
  );
}
