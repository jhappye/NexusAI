import type { FC } from 'react'
import { cn } from '@/utils/classnames'
import { basePath } from '@/utils/var'

type LogoEmbeddedChatHeaderProps = {
  className?: string
}

const LogoEmbeddedChatHeader: FC<LogoEmbeddedChatHeaderProps> = ({
  className,
}) => {
  return (
    <picture>
      <source media="(resolution: 1x)" srcSet="/logo/nexusai-logo.svg" />
      <source media="(resolution: 2x)" srcSet="/logo/nexusai-logo.svg" />
      <source media="(resolution: 3x)" srcSet="/logo/nexusai-logo.svg" />
      <img
        src={`${basePath}/logo/nexusai-logo.svg`}
        alt="logo"
        className={cn('block h-6 w-auto', className)}
      />
    </picture>
  )
}

export default LogoEmbeddedChatHeader
