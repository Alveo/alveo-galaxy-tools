#!/usr/bin/env cwl-runner
arguments:
- valueFrom:
    engine: '#galaxy_command_line'
    script: |-
      python
              alveo_api_key.py --api_key "$api_key" --output_path $output
baseCommand: [/bin/sh, -c]
class: CommandLineTool
inputs:
- {default: '', id: '#api_key', label: API Key, type: string}
- {default: output, id: '#output', type: string}
label: Store Alveo API Key
outputs:
- id: '#output_out'
  outputBinding: {glob: output}
  type: File
requirements:
- {class: ExpressionEngineRequirement, engineCommand: ./galaxy-command-line.py, id: '#galaxy_command_line'}
- {class: ExpressionEngineRequirement, engineCommand: ./galaxy-template.py, id: '#galaxy_template'}
- class: EnvVarRequirement
  envDef:
  - {envName: GALAXY_SLOTS, envValue: ''}
