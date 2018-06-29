import angular from 'angular';

import { AccountSettingsScreen } from './account-settings.screen';
import {appApi} from '../../api/app.api';

export let accountSettingsScreen = angular
  .module('awsec2-app.accountSettingsScreen', [
    appApi ])
  .component('accountSettingsScreen', AccountSettingsScreen)
  .config(['$httpProvider', '$locationProvider', function($httpProvider, djangoConstants) {
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	}])
  .name;