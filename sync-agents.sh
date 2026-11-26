#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_RULES_DIR="$SCRIPT_DIR/rules"
SOURCE_AGENTS_FILE="$SOURCE_RULES_DIR/baseline.md"
SOURCE_REFERENCES_DIR="$SOURCE_RULES_DIR/references"
SOURCE_CODEX_CONFIG_FILE="$SCRIPT_DIR/configs/codex/config.toml"
CODEX_CONFIG_MERGE_SCRIPT="$SCRIPT_DIR/scripts/merge_codex_config.py"
SOURCE_OPENCODE_CONFIG_FILE="$SCRIPT_DIR/configs/opencode/opencode.jsonc"
SOURCE_SKILLS_DIR="$SCRIPT_DIR/skills"
SOURCE_SHARED_SKILLS_DIR="$SOURCE_SKILLS_DIR/_shared"
SOURCE_SKILL_TARGETS_FILE="$SOURCE_SKILLS_DIR/targets.conf"
SKILL_TARGETS=(codex workbuddy opencode zcode qoder-cn dsh)
CODEX_ROOT="${CODEX_ROOT:-$HOME/.codex}"
WORKBUDDY_ROOT="${WORKBUDDY_ROOT:-$HOME/.workbuddy}"
OPENCODE_ROOT="${OPENCODE_ROOT:-$HOME/.config/opencode}"
ZCODE_ROOT="${ZCODE_ROOT:-$HOME/.zcode}"
QODER_CN_ROOT="${QODER_CN_ROOT:-$HOME/.qoder-cn}"
EXIT_SENTINEL="__SYNC_AGENTS_EXIT__"
ALL_SKILLS_SENTINEL="__SYNC_AGENTS_ALL_SKILLS__"

require_command() {
    local command_name="$1"

    if ! command_exists "$command_name"; then
        echo "$command_name is required but not installed" >&2
        exit 1
    fi
}

require_file() {
    local file_path="$1"
    local description="$2"

    if [[ ! -f "$file_path" ]]; then
        echo "$description not found: $file_path" >&2
        exit 1
    fi
}

require_dir() {
    local dir_path="$1"
    local description="$2"

    if [[ ! -d "$dir_path" ]]; then
        echo "$description not found: $dir_path" >&2
        exit 1
    fi
}

command_exists() {
    local command_name="$1"

    command -v "$command_name" >/dev/null 2>&1
}

sha256_file() {
    local file_path="$1"

    if command_exists sha256sum; then
        sha256sum "$file_path" | awk '{print $1}'
        return 0
    fi

    if command_exists shasum; then
        shasum -a 256 "$file_path" | awk '{print $1}'
        return 0
    fi

    if command_exists openssl; then
        openssl dgst -sha256 -r "$file_path" | awk '{print $1}'
        return 0
    fi

    echo "A SHA-256 tool is required but not installed (tried: sha256sum, shasum, openssl)" >&2
    exit 1
}

trim_spaces() {
    local value="$1"

    value="${value#"${value%%[![:space:]]*}"}"
    value="${value%"${value##*[![:space:]]}"}"
    printf '%s\n' "$value"
}

abort_closed_input() {
    echo "Standard input is closed (EOF); aborting." >&2
    exit 1
}

verify_file_copy() {
    local source_path="$1"
    local dest_path="$2"
    local source_hash=""
    local dest_hash=""

    source_hash="$(sha256_file "$source_path")"
    dest_hash="$(sha256_file "$dest_path")"

    if [[ "$source_hash" != "$dest_hash" ]]; then
        echo "sha256 verification failed for $dest_path" >&2
        exit 1
    fi
}

assert_safe_directory_dest() {
    local dest_path="$1"

    if [[ -z "$dest_path" || "$dest_path" == "/" || "$dest_path" == "$HOME" ]]; then
        echo "Refusing to replace unsafe directory path: $dest_path" >&2
        exit 1
    fi
}

sync_path() {
    local source_path="$1"
    local dest_path="$2"
    local dest_parent=""
    local base_name=""
    local staging_path=""

    dest_parent="$(dirname "$dest_path")"
    mkdir -p "$dest_parent"

    if [[ -f "$source_path" ]]; then
        install -m 0644 "$source_path" "$dest_path"
        verify_file_copy "$source_path" "$dest_path"
        echo "Synced file -> $dest_path"
        return 0
    fi

    if [[ ! -d "$source_path" ]]; then
        echo "Unsupported source path: $source_path" >&2
        exit 1
    fi

    assert_safe_directory_dest "$dest_path"
    base_name="$(basename "$dest_path")"
    staging_path="$(mktemp -d "$dest_parent/.${base_name}.XXXXXX")"
    cp -R "$source_path"/. "$staging_path"/
    rm -rf "$dest_path"
    mv "$staging_path" "$dest_path"

    if ! diff -qr "$source_path" "$dest_path" >/dev/null; then
        echo "directory verification failed for $dest_path" >&2
        exit 1
    fi

    echo "Synced directory -> $dest_path"
}

choose_content() {
    echo "Select content to sync:" >&2
    local content=""

    while true; do
        echo "1) rules" >&2
        echo "2) skills" >&2
        echo "3) config" >&2
        echo "4) exit" >&2
        if ! read -r -p "#? " content; then
            abort_closed_input
        fi
        content="$(trim_spaces "$content")"

        case "$content" in
            1|rules)
                printf '%s\n' "rules"
                return 0
                ;;
            2|skills)
                printf '%s\n' "skills"
                return 0
                ;;
            3|config|codex-config|opencode-config)
                printf '%s\n' "config"
                return 0
                ;;
            4|exit)
                printf '%s\n' "$EXIT_SENTINEL"
                return 0
                ;;
            *)
                echo "Invalid selection, try again." >&2
                ;;
        esac
    done
}

choose_rules_target() {
    echo "Select rules target:" >&2
    local target=""

    while true; do
        echo "1) codex -> AGENTS.md + references" >&2
        echo "2) workbuddy -> AGENTS.md + references" >&2
        echo "3) opencode -> AGENTS.md + references" >&2
        echo "4) zcode -> AGENTS.md + references" >&2
        echo "5) qoder-cn -> AGENTS.md + references" >&2
        echo "6) dsh -> AGENTS.md + references (DeepSeek Harness)" >&2
        echo "7) exit" >&2
        if ! read -r -p "#? " target; then
            abort_closed_input
        fi
        target="$(trim_spaces "$target")"

        case "$target" in
            1|codex)
                printf '%s\n' "codex"
                return 0
                ;;
            2|workbuddy)
                printf '%s\n' "workbuddy"
                return 0
                ;;
            3|opencode)
                printf '%s\n' "opencode"
                return 0
                ;;
            4|zcode)
                printf '%s\n' "zcode"
                return 0
                ;;
            5|qoder-cn)
                printf '%s\n' "qoder-cn"
                return 0
                ;;
            6|dsh|deepseek|deepseek-harness)
                printf '%s\n' "dsh"
                return 0
                ;;
            7|exit)
                printf '%s\n' "$EXIT_SENTINEL"
                return 0
                ;;
            *)
                echo "Invalid selection, try again." >&2
                ;;
        esac
    done
}

choose_config_target() {
    echo "Select config target:" >&2
    local target=""

    while true; do
        echo "1) codex -> config.toml" >&2
        echo "2) opencode -> opencode.jsonc" >&2
        echo "3) exit" >&2
        if ! read -r -p "#? " target; then
            abort_closed_input
        fi
        target="$(trim_spaces "$target")"

        case "$target" in
            1|codex)
                printf '%s\n' "codex"
                return 0
                ;;
            2|opencode)
                printf '%s\n' "opencode"
                return 0
                ;;
            3|exit)
                printf '%s\n' "$EXIT_SENTINEL"
                return 0
                ;;
            *)
                echo "Invalid selection, try again." >&2
                ;;
        esac
    done
}

choose_skill_target() {
    echo "Select target assistant:" >&2
    echo "dsh = DeepSeek Harness" >&2
    # Keep Bash's select menu in a single column.
    local COLUMNS=1
    local target=""

    select target in "${SKILL_TARGETS[@]}" "exit"; do
        case "$target" in
            "")
                echo "Invalid selection, try again." >&2
                ;;
            "exit")
                printf '%s\n' "$EXIT_SENTINEL"
                return 0
                ;;
            *)
                printf '%s\n' "$target"
                return 0
                ;;
        esac
    done

    abort_closed_input
}

resolve_skill_target_root() {
    local target="$1"

    case "$target" in
        codex)
            printf '%s\n' "$CODEX_ROOT"
            ;;
        workbuddy)
            printf '%s\n' "$WORKBUDDY_ROOT"
            ;;
        opencode)
            printf '%s\n' "$OPENCODE_ROOT"
            ;;
        zcode)
            printf '%s\n' "$ZCODE_ROOT"
            ;;
        qoder-cn)
            printf '%s\n' "$QODER_CN_ROOT"
            ;;
        dsh)
            printf '%s\n' "$HOME/.dsh"
            ;;
        *)
            echo "Unsupported target assistant: $target" >&2
            exit 1
            ;;
    esac
}

discover_compatible_skills() {
    local selected_target="$1"
    local skill_name=""
    local target_list=""
    local allowed_target=""
    local restricted_skills=" "
    local allowed_skills=" "
    local -a allowed_targets=()
    local skill_directories=""
    local skill_dir=""

    require_file "$SOURCE_SKILL_TARGETS_FILE" "Skill target restrictions file"
    while read -r skill_name target_list || [[ -n "$skill_name" ]]; do
        if [[ -z "$skill_name" || "$skill_name" == \#* ]]; then
            continue
        fi
        if [[ ! "$skill_name" =~ ^[a-z0-9][a-z0-9-]*$ ||
            ! -f "$SOURCE_SKILLS_DIR/$skill_name/SKILL.md" ||
            -L "$SOURCE_SKILLS_DIR/$skill_name" ]]; then
            echo "Unknown skill in $SOURCE_SKILL_TARGETS_FILE: $skill_name" >&2
            return 1
        fi
        if [[ -z "$target_list" || "$restricted_skills" == *" $skill_name "* ]]; then
            echo "Expected one nonempty target list for $skill_name in $SOURCE_SKILL_TARGETS_FILE" >&2
            return 1
        fi

        restricted_skills+="$skill_name "
        read -r -a allowed_targets <<< "$target_list"
        for allowed_target in "${allowed_targets[@]}"; do
            if [[ " ${SKILL_TARGETS[*]} " != *" $allowed_target "* ]]; then
                echo "Unknown target for $skill_name in $SOURCE_SKILL_TARGETS_FILE: $allowed_target" >&2
                return 1
            fi
            if [[ "$allowed_target" == "$selected_target" ]]; then
                allowed_skills+="$skill_name "
            fi
        done
    done < "$SOURCE_SKILL_TARGETS_FILE" || return 1

    skill_directories="$(find "$SOURCE_SKILLS_DIR" -mindepth 1 -maxdepth 1 -type d | sort)" || return 1
    while IFS= read -r skill_dir; do
        skill_name="${skill_dir##*/}"
        if [[ -f "$skill_dir/SKILL.md" && ( "$restricted_skills" != *" $skill_name "* ||
            "$allowed_skills" == *" $skill_name "* ) ]]; then
            printf '%s\n' "$skill_dir"
        fi
    done <<< "$skill_directories"
}

choose_skill() {
    local -a skill_names=()
    local skill_dir=""
    local selected_name=""

    for skill_dir in "$@"; do
        skill_names+=("${skill_dir##*/}")
    done

    echo "Available skills:" >&2
    select selected_name in "all" "${skill_names[@]}" "exit"; do
        case "$selected_name" in
            "")
                echo "Invalid selection, try again." >&2
                ;;
            "all")
                printf '%s\n' "$ALL_SKILLS_SENTINEL"
                return 0
                ;;
            "exit")
                printf '%s\n' "$EXIT_SENTINEL"
                return 0
                ;;
            *)
                printf '%s\n' "$SOURCE_SKILLS_DIR/$selected_name"
                return 0
                ;;
        esac
    done

    abort_closed_input
}

sync_agents_file() (
    local target_root="$1"
    local generated_dir=""

    mkdir -p -- "$target_root"
    target_root="$(
        cd -P -- "$target_root" || exit 1
        if [[ "$PWD" == *$'\n'* || "$PWD" == *$'\r'* ]]; then
            echo "Rules target path cannot contain line breaks." >&2
            exit 1
        fi
        printf '%s\n' "$PWD"
    )"
    generated_dir="$(mktemp -d "${TMPDIR:-/tmp}/sync-agents.XXXXXX")"
    trap 'rm -rf -- "$generated_dir"' EXIT

    {
        printf '```text\n'
        printf 'Installation metadata generated by sync-agents.sh.\n'
        printf 'Instruction file: %s/AGENTS.md\n' "$target_root"
        printf 'Reference root: %s/references/\n' "$target_root"
        printf '```\n\n'
        cat "$SOURCE_AGENTS_FILE"
    } > "$generated_dir/AGENTS.md"

    sync_path "$generated_dir/AGENTS.md" "$target_root/AGENTS.md"
    sync_path "$SOURCE_REFERENCES_DIR" "$target_root/references"
)

validated_root() {
    local target_root=""
    local target_variable="$2"

    target_root="$(trim_spaces "$1")"
    if [[ -z "$target_root" ]]; then
        echo "$target_variable cannot be empty." >&2
        exit 1
    fi

    printf '%s\n' "$target_root"
}

sync_global_rules_dir() {
    local target_root
    target_root="$(validated_root "$1" "$2")"
    sync_agents_file "$target_root"
}

sync_codex_config_file() {
    local target_root="$1"

    uv run --frozen --project "$SCRIPT_DIR" \
        python "$CODEX_CONFIG_MERGE_SCRIPT" \
        "$SOURCE_CODEX_CONFIG_FILE" \
        "$target_root/config.toml"
}

sync_skills() {
    local -a skills=()
    local -a selected_skills=()
    local skill=""
    local skill_paths=""
    local selected_skill=""
    local selected_target=""
    local target_root=""

    selected_target="$(choose_skill_target)"
    if [[ "$selected_target" == "$EXIT_SENTINEL" ]]; then
        exit 0
    fi

    skill_paths="$(discover_compatible_skills "$selected_target")"
    if [[ -z "$skill_paths" ]]; then
        echo "No compatible skills found for $selected_target under: $SOURCE_SKILLS_DIR" >&2
        return 1
    fi
    while IFS= read -r skill; do
        skills+=("$skill")
    done <<< "$skill_paths"

    selected_skill="$(choose_skill "${skills[@]}")"
    if [[ "$selected_skill" == "$EXIT_SENTINEL" ]]; then
        exit 0
    fi

    if [[ "$selected_skill" == "$ALL_SKILLS_SENTINEL" ]]; then
        selected_skills=("${skills[@]}")
    else
        selected_skills=("$selected_skill")
    fi

    target_root="$(resolve_skill_target_root "$selected_target")"
    sync_path "$SOURCE_SHARED_SKILLS_DIR" "$target_root/skills/_shared"
    for skill in "${selected_skills[@]}"; do
        sync_path "$skill" "$target_root/skills/${skill##*/}"
    done
}

main() {
    local content=""
    local rules_target=""
    local config_target=""

    if [[ $# -ne 0 ]]; then
        echo "This script is interactive and does not accept command-line arguments." >&2
        exit 1
    fi

    require_file "$SOURCE_AGENTS_FILE" "Codex AGENTS source file"
    require_file "$SOURCE_CODEX_CONFIG_FILE" "Codex config source file"
    require_file "$SOURCE_OPENCODE_CONFIG_FILE" "OpenCode config source file"
    require_dir "$SOURCE_RULES_DIR" "Rules source directory"
    require_dir "$SOURCE_REFERENCES_DIR" "Rules references source directory"
    require_dir "$SOURCE_SKILLS_DIR" "Skills source directory"
    require_dir "$SOURCE_SHARED_SKILLS_DIR" "Shared skills source directory"

    require_command diff

    content="$(choose_content)"
    if [[ "$content" == "$EXIT_SENTINEL" ]]; then
        exit 0
    fi

    if [[ "$content" == "skills" ]]; then
        sync_skills
        return 0
    fi

    if [[ "$content" == "config" ]]; then
        config_target="$(choose_config_target)"
        if [[ "$config_target" == "$EXIT_SENTINEL" ]]; then
            exit 0
        fi

        if [[ "$config_target" == "codex" ]]; then
            require_file "$CODEX_CONFIG_MERGE_SCRIPT" "Codex config merge script"
            require_command uv

            CODEX_ROOT="$(validated_root "$CODEX_ROOT" CODEX_ROOT)"

            sync_codex_config_file "$CODEX_ROOT"
            return 0
        fi

        OPENCODE_ROOT="$(validated_root "$OPENCODE_ROOT" OPENCODE_ROOT)"
        sync_path "$SOURCE_OPENCODE_CONFIG_FILE" "$OPENCODE_ROOT/opencode.jsonc"
        return 0
    fi

    rules_target="$(choose_rules_target)"
    if [[ "$rules_target" == "$EXIT_SENTINEL" ]]; then
        exit 0
    fi

    case "$rules_target" in
        codex)
            sync_global_rules_dir "$CODEX_ROOT" "CODEX_ROOT"
            ;;
        workbuddy)
            sync_global_rules_dir "$WORKBUDDY_ROOT" "WORKBUDDY_ROOT"
            ;;
        opencode)
            sync_global_rules_dir "$OPENCODE_ROOT" "OPENCODE_ROOT"
            ;;
        zcode)
            sync_global_rules_dir "$ZCODE_ROOT" "ZCODE_ROOT"
            ;;
        qoder-cn)
            sync_global_rules_dir "$QODER_CN_ROOT" "QODER_CN_ROOT"
            ;;
        dsh)
            sync_agents_file "$HOME/.dsh"
            ;;
        *)
            echo "Unsupported rules target: $rules_target" >&2
            exit 1
            ;;
    esac
}

main "$@"
