function GetOciTopLevelCommand_jms() {
    return 'jms'
}

function GetOciSubcommands_jms() {
    $ociSubcommands = @{
        'jms' = 'application-usage fleet fleet-agent-configuration installation-usage jre-usage managed-instance-usage work-request work-request-error work-request-log-entry'
        'jms application-usage' = 'request-summarized summarize'
        'jms fleet' = 'change-compartment create delete get list update'
        'jms fleet-agent-configuration' = 'get update'
        'jms installation-usage' = 'request-summarized summarize'
        'jms jre-usage' = 'request-summarized summarize'
        'jms managed-instance-usage' = 'request-summarized summarize'
        'jms work-request' = 'get list'
        'jms work-request-error' = 'list'
        'jms work-request-log-entry' = 'list-work-request-logs'
    }
    return $ociSubcommands
}

function GetOciCommandsToLongParams_jms() {
    $ociCommandsToLongParams = @{
        'jms application-usage request-summarized' = 'application-id application-type display-name fields fleet-id from-json help installation-path jre-distribution jre-vendor jre-version limit managed-instance-id page sort-by sort-order time-end time-start'
        'jms application-usage summarize' = 'application-id application-type display-name fields fleet-id from-json help installation-path jre-distribution jre-vendor jre-version limit managed-instance-id page sort-by sort-order time-end time-start'
        'jms fleet change-compartment' = 'compartment-id fleet-id from-json help if-match max-wait-seconds wait-for-state wait-interval-seconds'
        'jms fleet create' = 'compartment-id defined-tags description display-name freeform-tags from-json help max-wait-seconds wait-for-state wait-interval-seconds'
        'jms fleet delete' = 'fleet-id force from-json help if-match max-wait-seconds wait-for-state wait-interval-seconds'
        'jms fleet get' = 'fleet-id from-json help'
        'jms fleet list' = 'all compartment-id display-name from-json help id lifecycle-state limit page page-size sort-by sort-order'
        'jms fleet update' = 'defined-tags description display-name fleet-id force freeform-tags from-json help if-match max-wait-seconds wait-for-state wait-interval-seconds'
        'jms fleet-agent-configuration get' = 'fleet-id from-json help'
        'jms fleet-agent-configuration update' = 'fleet-id force from-json help if-match jre-scan-frequency jut-processing-frequency linux-configuration max-wait-seconds wait-for-state wait-interval-seconds windows-configuration'
        'jms installation-usage request-summarized' = 'application-id fields fleet-id from-json help installation-path jre-distribution jre-vendor jre-version limit managed-instance-id page sort-by sort-order time-end time-start'
        'jms installation-usage summarize' = 'application-id fields fleet-id from-json help installation-path jre-distribution jre-vendor jre-version limit managed-instance-id page sort-by sort-order time-end time-start'
        'jms jre-usage request-summarized' = 'application-id fields fleet-id from-json help jre-distribution jre-vendor jre-version limit managed-instance-id page sort-by sort-order time-end time-start'
        'jms jre-usage summarize' = 'application-id fields fleet-id from-json help jre-distribution jre-vendor jre-version limit managed-instance-id page sort-by sort-order time-end time-start'
        'jms managed-instance-usage request-summarized' = 'application-id fields fleet-id from-json help installation-path jre-distribution jre-vendor jre-version limit managed-instance-id managed-instance-type page sort-by sort-order time-end time-start'
        'jms managed-instance-usage summarize' = 'application-id fields fleet-id from-json help installation-path jre-distribution jre-vendor jre-version limit managed-instance-id managed-instance-type page sort-by sort-order time-end time-start'
        'jms work-request get' = 'from-json help work-request-id'
        'jms work-request list' = 'all compartment-id from-json help id limit page page-size'
        'jms work-request-error list' = 'all from-json help limit page page-size work-request-id'
        'jms work-request-log-entry list-work-request-logs' = 'all from-json help limit page page-size work-request-id'
    }
    return $ociCommandsToLongParams
}

function GetOciCommandsToShortParams_jms() {
    $ociCommandsToShortParams = @{
        'jms application-usage request-summarized' = '? h'
        'jms application-usage summarize' = '? h'
        'jms fleet change-compartment' = '? c h'
        'jms fleet create' = '? c h'
        'jms fleet delete' = '? h'
        'jms fleet get' = '? h'
        'jms fleet list' = '? c h'
        'jms fleet update' = '? h'
        'jms fleet-agent-configuration get' = '? h'
        'jms fleet-agent-configuration update' = '? h'
        'jms installation-usage request-summarized' = '? h'
        'jms installation-usage summarize' = '? h'
        'jms jre-usage request-summarized' = '? h'
        'jms jre-usage summarize' = '? h'
        'jms managed-instance-usage request-summarized' = '? h'
        'jms managed-instance-usage summarize' = '? h'
        'jms work-request get' = '? h'
        'jms work-request list' = '? c h'
        'jms work-request-error list' = '? h'
        'jms work-request-log-entry list-work-request-logs' = '? h'
    }
    return $ociCommandsToShortParams
}