/**
 * Tests for embedded-chatbot utility functions.
 */

import { isNexusAI } from '../utils'

describe('isNexusAI', () => {
  const originalReferrer = document.referrer

  afterEach(() => {
    Object.defineProperty(document, 'referrer', {
      value: originalReferrer,
      writable: true,
    })
  })

  it('should return true when referrer includes nexusai.ai', () => {
    Object.defineProperty(document, 'referrer', {
      value: 'https://nexusai.ai/something',
      writable: true,
    })

    expect(isNexusAI()).toBe(true)
  })

  it('should return true when referrer includes www.nexusai.ai', () => {
    Object.defineProperty(document, 'referrer', {
      value: 'https://www.nexusai.ai/app/xyz',
      writable: true,
    })

    expect(isNexusAI()).toBe(true)
  })

  it('should return false when referrer does not include nexusai.ai', () => {
    Object.defineProperty(document, 'referrer', {
      value: 'https://example.com',
      writable: true,
    })

    expect(isNexusAI()).toBe(false)
  })

  it('should return false when referrer is empty', () => {
    Object.defineProperty(document, 'referrer', {
      value: '',
      writable: true,
    })

    expect(isNexusAI()).toBe(false)
  })

  it('should return false when referrer does not contain nexusai.ai domain', () => {
    Object.defineProperty(document, 'referrer', {
      value: 'https://example-nexusai.com',
      writable: true,
    })

    expect(isNexusAI()).toBe(false)
  })

  it('should handle referrer without protocol', () => {
    Object.defineProperty(document, 'referrer', {
      value: 'nexusai.ai',
      writable: true,
    })

    expect(isNexusAI()).toBe(true)
  })

  it('should return true when referrer includes api.nexusai.ai', () => {
    Object.defineProperty(document, 'referrer', {
      value: 'https://api.nexusai.ai/v1/endpoint',
      writable: true,
    })

    expect(isNexusAI()).toBe(true)
  })

  it('should return true when referrer includes app.nexusai.ai', () => {
    Object.defineProperty(document, 'referrer', {
      value: 'https://app.nexusai.ai/chat',
      writable: true,
    })

    expect(isNexusAI()).toBe(true)
  })

  it('should return true when referrer includes docs.nexusai.ai', () => {
    Object.defineProperty(document, 'referrer', {
      value: 'https://docs.nexusai.ai/guide',
      writable: true,
    })

    expect(isNexusAI()).toBe(true)
  })

  it('should return true when referrer has nexusai.ai with query parameters', () => {
    Object.defineProperty(document, 'referrer', {
      value: 'https://nexusai.ai/?ref=test&id=123',
      writable: true,
    })

    expect(isNexusAI()).toBe(true)
  })

  it('should return true when referrer has nexusai.ai with hash fragment', () => {
    Object.defineProperty(document, 'referrer', {
      value: 'https://nexusai.ai/page#section',
      writable: true,
    })

    expect(isNexusAI()).toBe(true)
  })

  it('should return true when referrer has nexusai.ai with port number', () => {
    Object.defineProperty(document, 'referrer', {
      value: 'https://nexusai.ai:8080/app',
      writable: true,
    })

    expect(isNexusAI()).toBe(true)
  })

  it('should return true when nexusai.ai appears after another domain', () => {
    Object.defineProperty(document, 'referrer', {
      value: 'https://example.com/redirect?url=https://nexusai.ai',
      writable: true,
    })

    expect(isNexusAI()).toBe(true)
  })

  it('should return true when substring contains nexusai.ai', () => {
    Object.defineProperty(document, 'referrer', {
      value: 'https://notnexusai.ai',
      writable: true,
    })

    expect(isNexusAI()).toBe(true)
  })

  it('should return true when nexusai.ai is part of a different domain', () => {
    Object.defineProperty(document, 'referrer', {
      value: 'https://fake-nexusai.ai.example.com',
      writable: true,
    })

    expect(isNexusAI()).toBe(true)
  })

  it('should return true with multiple referrer variations', () => {
    const variations = [
      'https://nexusai.ai',
      'http://www.nexusai.ai',
      'http://nexusai.ai/',
      'https://nexusai.ai/app?token=123#section',
      'nexusai.ai/test',
      'www.nexusai.ai/en',
    ]

    variations.forEach((referrer) => {
      Object.defineProperty(document, 'referrer', {
        value: referrer,
        writable: true,
      })
      expect(isNexusAI()).toBe(true)
    })
  })

  it('should return false with multiple non-nexusai referrer variations', () => {
    const variations = [
      'https://github.com',
      'https://google.com',
      'https://stackoverflow.com',
      'https://example.nexusai',
      'https://nexusaiai.com',
      '',
    ]

    variations.forEach((referrer) => {
      Object.defineProperty(document, 'referrer', {
        value: referrer,
        writable: true,
      })
      expect(isNexusAI()).toBe(false)
    })
  })
})
