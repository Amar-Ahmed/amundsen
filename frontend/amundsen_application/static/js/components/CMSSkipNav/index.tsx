import React from 'react';

import './styles.scss';

type CMSSkipNavProps = {
  href: string;
  children: React.ReactNode;
};

export default function CMSSkipNav({ href, children }: CMSSkipNavProps) {
  return (
    <a className="skipNav" href={href}>
      {children}
    </a>
  );
}
