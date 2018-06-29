import angular from 'angular';

import  { appApi } from '../../api/app.api';

import { AccountListScreen } from './account-list.screen';

export let accountListScreen = angular
  .module('awsec2-app.accountListScreen', [
    appApi
  ])
  .component('accountListScreen', AccountListScreen)
  .name;