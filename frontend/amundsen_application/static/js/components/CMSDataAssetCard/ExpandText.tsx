import React, { useState } from 'react';
import { Modal } from 'react-bootstrap';

import CMSLink from 'components/CMSLinkify';

type CMSShowMoreTextProps = {
  title: string;
  text: string;
  limit?: number;
  className?: string;
};

export default function ExpandText({
  title,
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
  // const shownText =
  //   !isNeeded || isExpanded ? text : `${text.substring(0, limit)}${ellipsis}`;
  const shownText = `${text.substring(0, limit)}${ellipsis}`;

  return (
    <div className={className}>
      <span>
        <CMSLink text={shownText} />
      </span>
      {isNeeded && (
        <button
          className="display--inline-block btn btn-link"
          onClick={() => setIsExpanded(true)}
        >
          {'more'}
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
