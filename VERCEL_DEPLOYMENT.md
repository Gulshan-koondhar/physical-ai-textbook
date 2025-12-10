# Vercel Deployment Guide

This document explains how to deploy your Docusaurus site to Vercel with proper CSS styling.

## Configuration Changes

The following changes were made to support Vercel deployment:

1. **Base URL Configuration**: Changed from GitHub Pages format (`/physical-ai-textbook/`) to root path (`/`) using environment variables
2. **Environment-based URL Configuration**: Added environment variable support for different deployment platforms
3. **Build Script Update**: Modified the `vercel-build` script to use `cross-env` for reliable environment variable setting across platforms
4. **Dependency Added**: Added `cross-env` as a dev dependency for cross-platform environment variable support

## Environment Variables

The configuration now uses the `DEPLOYMENT_PLATFORM` environment variable:
- When `DEPLOYMENT_PLATFORM=vercel`: Uses root path (`/`) for assets and Vercel URL
- Otherwise: Uses GitHub Pages path (`/physical-ai-textbook/`) and GitHub Pages URL

## Vercel Setup

To deploy to Vercel:

1. Connect your GitHub repository to Vercel
2. Use the following build settings:
   - Build Command: `npm run vercel-build`
   - Output Directory: `build`
   - Install Command: `npm install`

## Troubleshooting

If CSS still doesn't load after deployment:

1. Verify that the build command is set to `npm run vercel-build`
2. Check that the build output directory is set to `build`
3. Ensure that the `baseUrl` in `docusaurus.config.js` is using the root path (`/`) when deployed to Vercel
4. Check browser developer tools for any 404 errors on CSS files

## Testing Locally

To test the Vercel configuration locally:
```bash
npm run vercel-build
npm run serve
```

## Notes

- The site is configured to work with both GitHub Pages and Vercel through environment variables
- The `trailingSlash` option is left undefined to let Vercel handle it automatically
- `cross-env` ensures consistent environment variable handling across different platforms
- Broken anchor warnings in the build output do not affect CSS styling