
APPLICATION_NAME = "DSO Tool"
REGEX_PATTERNS = {
    'stage' : r"^([a-zA-Z][a-zA-Z0-9]+)/?([0-9])?$",
    'parameter_key': r"^[a-zA-Z][.a-zA-Z0-9_-]*[a-zA-Z0-9]$",
    'secret_key': r"^[a-zA-Z][.a-zA-Z0-9_-]*[a-zA-ZA-Z0-9]$",
    'template_key': r"^[a-zA-Z][./a-zA-Z0-9_-]*[a-zA-Z0-9]$",
}

MESSAGES = {
    'InvalidKeyPattern': "'{0}' is an invalid key. Must conform to '{1}'.",
    'InvalidKeyStr': "'{0}' is an invalid key. Cannot contain '{1}'.",
    'ParameterNotFound': "Parameter '{0}' not found in the given context.",
    'SecretNotFound': "Secret '{0}' not found in the given context.",
    'InvalidStage': "'{0}' is not a valid stage name. Valid form is <string>[/number], where it must conform to '{1}'.",
    'ContextNotFound': "Context '{0}' not found.",
    'PatternNotMatched': "'{0}' is invalid. Must conform to '{1}'",
    'InvalidParameterKeyValuePair': "'{0}' is an invalid parameter key/value pair. Must conform to '^([a-zA-Z][a-zA-Z0-9_.-/]*)=(.*)$'",
    'InvalidParameterKey': "'{0}' is an invalid parameter key. Must conform to '{1}'",
    'TemplateNotFound': "Template '{0}' not found.",
    'InvalidTemplateKey': "'{0}' is an invalid template key. Must conform to '{1}'",
    'ContextNotFoundListingInherited': "Context '{0}' not found, listing inherited parameters if any.",
    'OptionMutualInclusive': "Option {0} needed when {1} is provided.",
    'InvalidDSOConfigurationFile': "'{0}' is not a valid DSO configuration file.",
    'ProviderNotSet': "{0} provider has not been set.",
    'InvalidDSOConfigOverrides': "Invalid DSO configuration overrides. Must conform to '<key>=<value>, ...'",
    'DSOConfigutrationOverriden': "DSO configuration '{0}' overriden to '{1}'.",
    'DSOConfigNewer': "Application is configured to use a newer version of dso, expected '{0}', got '{1}'.",
    'DSOConfigOlder': "Application is configured to use an older version of dso, expected '{0}', got '{1}'.",
    'DSOConfigurationNotFound': 'DSO configuration not found.',
    'NoDSOConfigFound': "No DSO configuration found in the working directory.",
    'EnteredSecretValuesNotMatched': "Entered values for the secret did not macth.",
    'QueryOptionCompatibleFormats': "Option '-q' / '--query' can be used only with 'json'/'yaml' output formats.",
    'QueryAllOptionNonCompatibleFormats': "Option '-a'/ '--query-all' cannot be used with 'shell' output format.",
}
