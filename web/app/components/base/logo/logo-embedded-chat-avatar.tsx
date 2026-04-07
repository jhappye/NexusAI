import type { FC } from 'react'
import { basePath } from '@/utils/var'

type LogoEmbeddedChatAvatarProps = {
  className?: string
}
const LogoEmbeddedChatAvatar: FC<LogoEmbeddedChatAvatarProps> = ({
  className,
}) => {
  return (
    <img
      src={`${basePath}/logo/nexusai-logo.svg`}
      className={`block h-10 w-10 ${className}`}
      alt="logo"
    />
  )
}

export default LogoEmbeddedChatAvatar
