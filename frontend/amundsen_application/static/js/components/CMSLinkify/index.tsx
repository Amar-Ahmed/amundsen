import * as React from 'react';

type LinkEmailProps = {
  text: string;
};

/**
 * Parses out email addresses and surrounds them by anchor tags
 */
export default function LinkEmail({ text }: LinkEmailProps) {
  const [content, setContent] = React.useState<React.ReactNode[]>([]);

  React.useEffect(() => {
    const emailRegex = /([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)/g;
    const parts: (string | React.ReactNode)[] = text.split(emailRegex);

    for (let i = 1; i < parts.length; i += 2) {
      const link: string = parts[i] as string;
      parts[i] = (
        <a id={`email-anchor-${link}`} key={'link' + i} href={`mailto:${link}`}>
          {link}
        </a>
      );
    }

    setContent(parts);
  }, [text]);

  return <>{content}</>;
}
