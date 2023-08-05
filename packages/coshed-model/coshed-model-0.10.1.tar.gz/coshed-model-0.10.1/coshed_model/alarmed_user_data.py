#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import pendulum
from djali.dynamodb import DynamoController
from coshed_model.naming import environment_specific_name


TID = "alarm_latest_occurrence"
DEFAULT_ENV_NAME = "prod"
DEFAULT_REGION = "eu-central-1"
DEFAULT_TABLE_DATA = "alarmed"
DEFAULT_TABLE_RULESET = "alarmed_id"

DATASET_VERSION = 3


class UserDataControl:
    def __init__(self, user_id, namespaces=None, *args, **kwargs):
        if namespaces is None:
            namespaces = ()
        self.log = logging.getLogger(__name__)
        table_data = kwargs.get("table_data", DEFAULT_TABLE_DATA)
        table_ruleset = kwargs.get("table_ruleset", DEFAULT_TABLE_RULESET)
        region_name = kwargs.get("region_name", DEFAULT_REGION)
        self.env_name = kwargs.get("env_name", DEFAULT_ENV_NAME)
        self.user_id = str(user_id)
        self.namespaces = namespaces
        self.dc_data = DynamoController(table_data, region_name=region_name)
        self.dc_ruleset = DynamoController(table_ruleset, region_name=region_name)
        self.user_data = dict()
        self.user_rulesets = dict()

    @property
    def data_key(self):
        return environment_specific_name(
            "user-settings-{user_id}".format(user_id=self.user_id),
            env_name=self.env_name,
        )

    @property
    def data(self):
        if "dt" in self.user_data:
            self._sanitise_user_data_structure()
            return self.user_data

        self.load()

        return self.user_data

    def _sanitise_user_data_structure(self):
        try:
            self.user_data[TID]
        except KeyError:
            self.user_data[TID] = dict()

        for namespace in self.namespaces:
            try:
                self.user_data[TID][namespace]
            except KeyError:
                self.user_data[TID][namespace] = dict()

        self.user_data["version"] = DATASET_VERSION
        self.user_data["user_id"] = self.user_id

    def generate_ruleset_key(self, namespace):
        derived = environment_specific_name(self.user_id, env_name=self.env_name)
        return ".".join((namespace, derived))

    def __str__(self):
        portions = ["<{klass}".format(klass=self.__class__.__name__), self.data_key]
        for key in sorted(self.namespaces):
            portions.append(
                "{key}={val}".format(key=key, val=self.generate_ruleset_key(key))
            )
        return " ".join(portions) + ">"

    def _fetch_ruleset(self, namespace):
        key = self.generate_ruleset_key(namespace)
        self.log.info(
            "Fetching ruleset for {namespace}: {key!r}".format(
                namespace=namespace, key=key
            )
        )
        data = self.dc_ruleset[key]

        return data

    def load(self):
        default_data = dict(
            dt=pendulum.now().to_rfc3339_string(), version=3, user_id=self.user_id
        )

        try:
            data = self.dc_data[self.data_key]
            self.log.info(
                "Loaded data using {data_key!r}".format(data_key=self.data_key)
            )
        except KeyError:
            data = default_data
            self.log.warning(
                "No data available using {data_key!r}. Using default!".format(
                    data_key=self.data_key
                )
            )

        self.user_data = data
        self._sanitise_user_data_structure()

    def save(self):
        self.log.info("Saving data using {data_key!r}".format(data_key=self.data_key))
        self.user_data["dt"] = pendulum.now().to_rfc3339_string()
        self.dc_data[self.data_key] = self.user_data

    def drop(self):
        self.log.info("Dropping data using {data_key!r}".format(data_key=self.data_key))

        try:
            del self.dc_data[self.data_key]
        except KeyError:
            pass

    def __getitem__(self, key):
        if key in self.namespaces:
            try:
                return self.user_rulesets[key]
            except KeyError:
                try:
                    self.user_rulesets[key] = self._fetch_ruleset(key)
                except KeyError:
                    self.user_rulesets[key] = dict()

                return self.user_rulesets[key]

    def get_latest_occurrence(self, alarm_id, namespace, serial_number):
        rv = None

        self.log.info(
            "Retrieve latest occurrence for {alarm_id!r} on [{namespace}] {serial_number}".format(
                alarm_id=alarm_id, namespace=namespace, serial_number=serial_number
            )
        )

        try:
            rv = pendulum.parse(self.data[TID][namespace][alarm_id][serial_number])
        except KeyError:
            pass
        except Exception as exc:
            self.log.warning(exc)

        self.log.info("-> {!r}".format(rv))

        return rv

    def set_latest_occurrence(self, alarm_id, occurrence, namespace, serial_number):
        v = occurrence.to_rfc3339_string()

        self.log.info(
            "Set latest occurrence for {alarm_id!r} on [{namespace}] {serial_number}: {value}".format(
                alarm_id=alarm_id,
                namespace=namespace,
                serial_number=serial_number,
                value=v,
            )
        )

        try:
            self.data[TID][namespace][alarm_id][serial_number]
        except KeyError:
            self._sanitise_user_data_structure()
            self.data[TID][namespace][alarm_id] = dict()
        except Exception as exc:
            self.log.error(
                "Oh, FUCK. Cannot set up data dictionary. This won't end well."
            )
            self.log.error(exc)

        self.data[TID][namespace][alarm_id][serial_number] = v
