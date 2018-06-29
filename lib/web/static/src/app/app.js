import angular from 'angular';
import uiRouter from 'angular-ui-router';
import angularMaterial from 'angular-material';
import angularMessages from 'angular-messages';

import { appToolbar } from 'yellowant-common-client/src/angularjs/components/app-toolbar/app-toolbar';

import { angularMaterialConfig } from 'yellowant-common-client/src/angularjs/config/angular-material.config';

import  { appApi } from './api/app.api';

import { AppComponent } from './app.component';
//import
import { accountListScreen } from './screens/account-list/account-list';
import { accountSettingsScreen } from './screens/account-settings/account-settings';
//import { awsauthoriseScreen } from './screens/account-authorize/account-settings';

export let twitterApp = angular
  .module('awsec2-app', [
    angularMaterial,
    uiRouter,
    appToolbar,
    angularMaterialConfig,
    appApi,
    accountListScreen,
    accountSettingsScreen,
    angularMessages
  ])
  .config(routeConfig)
  .factory('UserAccounts', UserAccounts)
  .component('yellowantAwsec2App', AppComponent)
  .name;

function UserAccounts(){
return {
    accountList : null
    }
}
routeConfig.$inject = ['$locationProvider', '$stateProvider', '$urlRouterProvider'];
function routeConfig($locationProvider, $stateProvider, $urlRouterProvider) {
  $locationProvider.html5Mode(true);
  $urlRouterProvider.otherwise('/')

  var accountListState = {
    name: 'accountList',
    url: '/',
    component: 'accountListScreen'
  };



  var accountSettingsState = {
    name: 'accountSettings',
    url: '/accounts/{accountId}',
    component: 'accountSettingsScreen'
  };

//  var awsauthorise = {
//    name: 'awsauthorise',
//    url: '/awsauthorise/{accountId}',
//    component: 'awsauthoriSescreen'
//  };

  $stateProvider.state(accountListState);
  $stateProvider.state(accountSettingsState);
  
}