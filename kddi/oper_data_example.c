/**
 * @file oper_data_example.c
 * @author Rastislav Szabo <raszabo@cisco.com>, Lukas Macko <lmacko@cisco.com>
 * @brief Example usage operational data API.
 *
 * @copyright
 * Copyright 2016 Cisco Systems, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>
#include <inttypes.h>

#include "sysrepo.h"
#include "sysrepo/values.h"
#include "sysrepo/xpath.h"

volatile int exit_application = 0;

static int
data_provider_cb(const char *xpath, sr_val_t **values, size_t *values_cnt, void *private_ctx)
{
    sr_val_t *v = NULL;
    int rc = SR_ERR_OK;

    printf("Data for '%s' requested.\n", xpath);      

    if (sr_xpath_node_name_eq(xpath, "slice")) {

        // allocate space for data to return
        rc = sr_new_values(34, &v);
        if (SR_ERR_OK != rc) {
            return rc;
        }

        sr_val_set_xpath(&v[0], "/sliceable-transceiver-sdm:transceiver-state/slice/sliceid");
        sr_val_set_str_data(&v[0], SR_STRING_T, "1");

        sr_val_set_xpath(&v[1], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal/opticalchannelid");
        sr_val_set_str_data(&v[1], SR_STRING_T, "1");
        sr_val_set_xpath(&v[2], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal[opticalchannelid='1']/monitor/osnr");

        sr_val_set_xpath(&v[3], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal/opticalchannelid");
        sr_val_set_str_data(&v[3], SR_STRING_T, "2");
        sr_val_set_xpath(&v[4], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal[opticalchannelid='2']/monitor/osnr");

        sr_val_set_xpath(&v[5], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal/opticalchannelid");
        sr_val_set_str_data(&v[5], SR_STRING_T, "3");
        sr_val_set_xpath(&v[6], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal[opticalchannelid='3']/monitor/osnr");

        sr_val_set_xpath(&v[7], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal/opticalchannelid");
        sr_val_set_str_data(&v[7], SR_STRING_T, "4");
        sr_val_set_xpath(&v[8], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal[opticalchannelid='4']/monitor/osnr");

        sr_val_set_xpath(&v[9], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal/opticalchannelid");
        sr_val_set_str_data(&v[9], SR_STRING_T, "5");
        sr_val_set_xpath(&v[10], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal[opticalchannelid='5']/monitor/osnr");

        sr_val_set_xpath(&v[11], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal/opticalchannelid");
        sr_val_set_str_data(&v[11], SR_STRING_T, "6");
        sr_val_set_xpath(&v[12], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal[opticalchannelid='6']/monitor/osnr");

        sr_val_set_xpath(&v[13], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal/opticalchannelid");
        sr_val_set_str_data(&v[13], SR_STRING_T, "7");
        sr_val_set_xpath(&v[14], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal[opticalchannelid='7']/monitor/osnr");

        sr_val_set_xpath(&v[15], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal/opticalchannelid");
        sr_val_set_str_data(&v[15], SR_STRING_T, "8");
        sr_val_set_xpath(&v[16], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal[opticalchannelid='8']/monitor/osnr");

        sr_val_set_xpath(&v[17], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal/opticalchannelid");
        sr_val_set_str_data(&v[17], SR_STRING_T, "9");
        sr_val_set_xpath(&v[18], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal[opticalchannelid='9']/monitor/osnr");
        sr_val_set_xpath(&v[19], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal[opticalchannelid='9']/monitor/ber");

        sr_val_set_xpath(&v[20], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal/opticalchannelid");
        sr_val_set_str_data(&v[20], SR_STRING_T, "10");
        sr_val_set_xpath(&v[21], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal[opticalchannelid='10']/monitor/osnr");

        sr_val_set_xpath(&v[22], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal/opticalchannelid");
        sr_val_set_str_data(&v[22], SR_STRING_T, "11");
        sr_val_set_xpath(&v[23], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal[opticalchannelid='11']/monitor/osnr");

        sr_val_set_xpath(&v[24], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal/opticalchannelid");
        sr_val_set_str_data(&v[24], SR_STRING_T, "12");
        sr_val_set_xpath(&v[25], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal[opticalchannelid='12']/monitor/osnr");

        sr_val_set_xpath(&v[26], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal/opticalchannelid");
        sr_val_set_str_data(&v[26], SR_STRING_T, "13");
        sr_val_set_xpath(&v[27], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal[opticalchannelid='13']/monitor/osnr");

        sr_val_set_xpath(&v[28], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal/opticalchannelid");
        sr_val_set_str_data(&v[28], SR_STRING_T, "14");
        sr_val_set_xpath(&v[29], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal[opticalchannelid='14']/monitor/osnr");

        sr_val_set_xpath(&v[30], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal/opticalchannelid");
        sr_val_set_str_data(&v[30], SR_STRING_T, "15");
        sr_val_set_xpath(&v[31], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal[opticalchannelid='15']/monitor/osnr");

        sr_val_set_xpath(&v[32], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal/opticalchannelid");
        sr_val_set_str_data(&v[32], SR_STRING_T, "16");
        sr_val_set_xpath(&v[33], "/sliceable-transceiver-sdm:transceiver-state/slice[sliceid='1']/optical-signal[opticalchannelid='16']/monitor/osnr");

        *values = v;
        *values_cnt = 34;

    } else {
        *values = NULL;
        values_cnt = 0;
    }

    return SR_ERR_OK;
}

static void
sigint_handler(int signum)
{
    exit_application = 1;
}

static int
data_provider(sr_session_ctx_t *session)
{
    sr_subscription_ctx_t *subscription = NULL;
    int rc = SR_ERR_OK;

    /* subscribe for providing operational data */
    // rc = sr_dp_get_items_subscribe(session, "/ietf-interfaces:interfaces-state", data_provider_cb, NULL, SR_SUBSCR_DEFAULT, &subscription);
    rc = sr_dp_get_items_subscribe(session, "/sliceable-transceiver-sdm:transceiver-state", data_provider_cb, NULL, SR_SUBSCR_DEFAULT, &subscription);
    if (SR_ERR_OK != rc) {
        fprintf(stderr, "Error by sr_dp_get_items_subscribe: %s\n", sr_strerror(rc));
        goto cleanup;
    }

    printf("\n\n ========== SUBSCRIBED FOR PROVIDING OPER DATA ==========\n\n");

    /* loop until ctrl-c is pressed / SIGINT is received */
    signal(SIGINT, sigint_handler);
    signal(SIGPIPE, SIG_IGN);
    while (!exit_application) {
        sleep(1000);
    }


    printf("Application exit requested, exiting.\n");

cleanup:
    if (NULL != subscription) {
        sr_unsubscribe(session, subscription);
    }
    return rc;
}



int
main(int argc, char **argv)
{
    sr_conn_ctx_t *connection = NULL;
    sr_session_ctx_t *session = NULL;
    int rc = SR_ERR_OK;

    /* connect to sysrepo */
    rc = sr_connect("example_application", SR_CONN_DEFAULT, &connection);
    if (SR_ERR_OK != rc) {
        fprintf(stderr, "Error by sr_connect: %s\n", sr_strerror(rc));
        goto cleanup;
    }

    /* start session */
    rc = sr_session_start(connection, SR_DS_RUNNING, SR_SESS_DEFAULT, &session);
    if (SR_ERR_OK != rc) {
        fprintf(stderr, "Error by sr_session_start: %s\n", sr_strerror(rc));
        goto cleanup;
    }

    /* run as a data provider */
    printf("This application will be a data provider for state data of sliceable-transceiver-sdm.\n");
    rc = data_provider(session);

cleanup:
    if (NULL != session) {
        sr_session_stop(session);
    }
    if (NULL != connection) {
        sr_disconnect(connection);
    }
    return rc;
}