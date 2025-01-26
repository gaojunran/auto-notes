/* eslint-disable */
/* prettier-ignore */
// @ts-nocheck
// Generated by unplugin-vue-router. ‼️ DO NOT MODIFY THIS FILE ‼️
// It's recommended to commit this file.
// Make sure to add this file to your tsconfig.json file as an "includes" or "files" entry.

declare module 'vue-router/auto-routes' {
  import type {
    RouteRecordInfo,
    ParamValue,
    ParamValueOneOrMore,
    ParamValueZeroOrMore,
    ParamValueZeroOrOne,
  } from 'vue-router'

  /**
   * Route name map generated by unplugin-vue-router
   */
  export interface RouteNamedMap {
    '/': RouteRecordInfo<'/', '/', Record<never, never>, Record<never, never>>,
    '/detail': RouteRecordInfo<'/detail', '/detail', Record<never, never>, Record<never, never>>,
    '/detail/connect': RouteRecordInfo<'/detail/connect', '/detail/connect', Record<never, never>, Record<never, never>>,
    '/detail/exercise/[id]': RouteRecordInfo<'/detail/exercise/[id]', '/detail/exercise/:id', { id: ParamValue<true> }, { id: ParamValue<false> }>,
    '/detail/note/[id]/': RouteRecordInfo<'/detail/note/[id]/', '/detail/note/:id', { id: ParamValue<true> }, { id: ParamValue<false> }>,
    '/detail/note/[id]/overview': RouteRecordInfo<'/detail/note/[id]/overview', '/detail/note/:id/overview', { id: ParamValue<true> }, { id: ParamValue<false> }>,
    '/detail/recognition/[id]': RouteRecordInfo<'/detail/recognition/[id]', '/detail/recognition/:id', { id: ParamValue<true> }, { id: ParamValue<false> }>,
    '/detail/thought/[id]': RouteRecordInfo<'/detail/thought/[id]', '/detail/thought/:id', { id: ParamValue<true> }, { id: ParamValue<false> }>,
    '/network': RouteRecordInfo<'/network', '/network', Record<never, never>, Record<never, never>>,
    '/NotFound': RouteRecordInfo<'/NotFound', '/NotFound', Record<never, never>, Record<never, never>>,
    '/quickjump': RouteRecordInfo<'/quickjump', '/quickjump', Record<never, never>, Record<never, never>>,
    '/record': RouteRecordInfo<'/record', '/record', Record<never, never>, Record<never, never>>,
    '/settings': RouteRecordInfo<'/settings', '/settings', Record<never, never>, Record<never, never>>,
    '/upload': RouteRecordInfo<'/upload', '/upload', Record<never, never>, Record<never, never>>,
  }
}
