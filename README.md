**Chain-Translator** is a Python script that automates a chain of Google translations, with the aim of generating comedic results. The script is highly configurable and able to easily adapt to different use cases.

The available configurations are listed below:

## translate_list.txt
`translate_list.txt` contains the strings the user wishes to translate, separated by line.

## config.json
`config.json` contains several configurations for the translator.
- `base_language` determines the starting language of the translator. Usually, this should be set to the same language as the strings in `translate_list.txt`. This also determines the language of the final output for each translated string. Defaults to `en`, for English.
- `language_chain` determines what languages are used in each translation chain.
- `translate_back_to_base_each_time` determines whether each step in the translation chain is translated back to the language specified by `base_language`. Note that the final output will still be in the base language regardless of this setting. Defaults to `true`.
- `randomize_chain_for_each_string` randomizes the order of the languages specified by `language_chain` for each translated string. Defaults to `false`.
- `print_all_available_languages` is a utility that prints every available language, along with its language code, for use in `base_language` and `language_chain`. Note that if this is set to `true`, no actual translations will be done. Defaults to `false`.
