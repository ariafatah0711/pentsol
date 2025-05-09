import telebot
from telebot import types
from config import MESSAGES, BOT_TOKEN, DATA_FILE, SEARCH_ALGORITHMS, DEFAULT_ALGORITHM
from utils.search import SearchEngine
import logging
import io
import pandas as pd
from datetime import datetime
import json
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def escape_markdown_v2(text: str) -> str:
    """Escapes characters for Telegram MarkdownV2 compliance."""
    text = str(text)
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    text = text.replace('\\', '\\\\')
    for char in escape_chars:
        text = text.replace(char, f'\\{char}')
    return text

class BoyerMoore:
    def __init__(self, pattern):
        self.pattern = pattern.lower()
        self.bad_char = self._bad_character_rule()
        self.good_suffix = self._good_suffix_rule()

    def _bad_character_rule(self):
        bad_char = {}
        for i, char in enumerate(self.pattern):
            bad_char[char] = i
        return bad_char

    def _good_suffix_rule(self):
        m = len(self.pattern)
        good_suffix = [0] * (m + 1)
        suffix = [0] * (m + 1)

        # Case 1: Exact match
        suffix[m] = m
        for i in range(m - 1, -1, -1):
            j = 0
            while j < i and self.pattern[i - j] == self.pattern[m - 1 - j]:
                j += 1
            suffix[i] = j

        # Case 2: Good suffix exists
        for i in range(m):
            good_suffix[i] = m
        j = 0
        for i in range(m - 1, -1, -1):
            if suffix[i] == i + 1:
                while j < m - 1 - i:
                    if good_suffix[j] == m:
                        good_suffix[j] = m - 1 - i
                    j += 1

        # Case 3: Good suffix doesn't exist
        for i in range(m - 1):
            good_suffix[m - 1 - suffix[i]] = m - 1 - i

        return good_suffix

    def search(self, text):
        text = text.lower()
        m = len(self.pattern)
        n = len(text)
        matches = []

        if m == 0 or n == 0:
            return matches

        i = m - 1
        while i < n:
            j = m - 1
            k = i
            while j >= 0 and text[k] == self.pattern[j]:
                j -= 1
                k -= 1

            if j == -1:
                matches.append(k + 1)
                i += 1
            else:
                bad_char_shift = j - self.bad_char.get(text[k], -1)
                good_suffix_shift = self.good_suffix[j + 1]
                i += max(bad_char_shift, good_suffix_shift)

        return matches

class KMP:
    def __init__(self, pattern):
        self.pattern = pattern.lower()
        self.lps = self._compute_lps()

    def _compute_lps(self):
        m = len(self.pattern)
        lps = [0] * m
        length = 0
        i = 1

        while i < m:
            if self.pattern[i] == self.pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1

        return lps

    def search(self, text):
        text = text.lower()
        m = len(self.pattern)
        n = len(text)
        matches = []

        if m == 0 or n == 0:
            return matches

        i = 0  # index for text
        j = 0  # index for pattern

        while i < n:
            if self.pattern[j] == text[i]:
                i += 1
                j += 1

            if j == m:
                matches.append(i - j)
                j = self.lps[j - 1]
            elif i < n and self.pattern[j] != text[i]:
                if j != 0:
                    j = self.lps[j - 1]
                else:
                    i += 1

        return matches

def register_handlers():
    bot = telebot.TeleBot(BOT_TOKEN)
    search_engine = SearchEngine()

    @bot.message_handler(commands=['start', 'help'])
    def handle_start_help(message):
        """Handle /start and /help commands"""
        try:
            logger.info(f"User {message.from_user.username} {message.text}")
            response = MESSAGES['welcome'] if message.text == '/start' else MESSAGES['help']
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row(types.KeyboardButton("/search"))
            markup.row(types.KeyboardButton("/describe"))
            markup.row(types.KeyboardButton("/create_solusi"))
            markup.row(types.KeyboardButton("/list"))
            bot.reply_to(
                message,
                escape_markdown_v2(response),
                parse_mode='MarkdownV2',
                reply_markup=markup
            )
        except Exception as e:
            bot.reply_to(message, f"❌ Error: {escape_markdown_v2(str(e))}")

    @bot.message_handler(commands=['search'])
    def handle_search(message):
        """Handle /search command"""
        try:
            query = message.text[8:].strip()
            logger.info(f"User {message.from_user.username} /search {query}")
            if not query:    
                bot.reply_to(message, MESSAGES['errors']['search_empty'], parse_mode='MarkdownV2')
                return
            results = search_engine.search(query)
            if not results:
                bot.reply_to(
                    message,
                    MESSAGES['errors']['search_not_found'].format(query=escape_markdown_v2(query)),
                    parse_mode='MarkdownV2'
                )
                return
            text = "*🔍 Search Results:*\n\n"
            markup = types.InlineKeyboardMarkup(row_width=2)
            buttons = []
            for result in results:
                technique = result['technique']
                score = result['score']
                escaped_name = escape_markdown_v2(technique['name'])
                text += f"• `{escaped_name}` \\(Match: {score}%\\)\n"
                buttons.append(
                    types.InlineKeyboardButton(
                        f"📖 {technique['name'][:20]}...",
                        callback_data=f"describe_{technique['id']}_search"
                    )
                )
            markup.add(*buttons)
            bot.reply_to(
                message,
                text,
                parse_mode='MarkdownV2',
                reply_markup=markup
            )
        except Exception as e:
            bot.reply_to(message, f"❌ Error: {escape_markdown_v2(str(e))}")

    @bot.message_handler(commands=['list'])
    def handle_list(message):
        """Handle /list command"""
        try:
            logger.info(f"User {message.from_user.username} {message.text}")
            categories = search_engine.get_categories()
            text = "*📜 Categories:*\n\n"
            markup = types.InlineKeyboardMarkup(row_width=2)
            buttons = []
            for category in categories:
                escaped_category = escape_markdown_v2(category)
                text += f"• `{escaped_category}`\n"
                buttons.append(
                    types.InlineKeyboardButton(
                        f"🔍 {category}",
                        callback_data=f"category_{category.lower().replace(' ', '_')}"
                    )
                )
            markup.add(*buttons)
            markup.add(types.InlineKeyboardButton("⬅️ Back to Menu", callback_data="back_to_menu"))
            bot.reply_to(
                message,
                text,
                parse_mode='MarkdownV2',
                reply_markup=markup
            )
        except Exception as e:
            bot.reply_to(message, f"❌ Error: {escape_markdown_v2(str(e))}")

    @bot.message_handler(commands=['create_solusi'])
    def handle_create_solusi(message):
        """Handle /create_solusi command to generate and send solutions in CSV format"""
        try:
            args = message.text[len('/create_solusi'):].strip().split(',')
            technique_names = [name.strip() for name in args if name.strip()]
            
            if not technique_names:
                bot.reply_to(
                    message,
                    MESSAGES['errors']['create_solusi_empty'],
                    parse_mode='MarkdownV2'
                )
                return

            techniques = []
            for name in technique_names:
                results = search_engine.search(name)
                if results:
                    techniques.append(results[0]['technique'])
                else:
                    bot.reply_to(
                        message,
                        MESSAGES['errors']['technique_not_found'].format(
                            name=escape_markdown_v2(name)
                        ),
                        parse_mode='MarkdownV2'
                    )
                    return

            # Create CSV data
            csv_dict = {}
            max_solutions = 0

            for tech in techniques:
                tech_name = tech['name']
                solutions = tech.get('solutions', [])
                if not isinstance(solutions, list):
                    solutions = [str(solutions)]
                csv_dict[tech_name] = solutions
                if len(solutions) > max_solutions:
                    max_solutions = len(solutions)

            columns = ['Technique'] + [f'Solution {i+1}' for i in range(max_solutions)]
            csv_data = []
            for name, solutions in csv_dict.items():
                row = [name] + solutions + ['-'] * (max_solutions - len(solutions))
                csv_data.append(row)

            df = pd.DataFrame(csv_data, columns=columns)
            output = io.StringIO()
            df.to_csv(output, index=False, encoding='utf-8')
            output.seek(0)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'solutions_{timestamp}.csv'

            bot.send_document(
                message.chat.id,
                (filename, output.getvalue().encode('utf-8')),
                caption=(
                    f"✅ Solutions for techniques: {', '.join([escape_markdown_v2(t['name']) for t in techniques])}"
                ),
                parse_mode='MarkdownV2'
            )

        except Exception as e:
            bot.reply_to(
                message,
                f"❌ Error: {escape_markdown_v2(str(e))}",
                parse_mode='MarkdownV2'
            )

    @bot.message_handler(commands=['describe'])
    def handle_describe(message):
        """Handle /describe command"""
        try:
            args = message.text[len('/describe'):].strip().split(',')
            technique_names = [name.strip() for name in args if name.strip()]
            
            if not technique_names:
                bot.reply_to(
                    message,
                    MESSAGES['errors']['describe_empty'],
                    parse_mode='MarkdownV2'
                )
                return

            for name in technique_names:
                results = search_engine.search(name)
                if not results:
                    bot.reply_to(
                        message,
                        MESSAGES['errors']['technique_not_found'].format(
                            name=escape_markdown_v2(name)
                        ),
                        parse_mode='MarkdownV2'
                    )
                    continue

                technique = results[0]['technique']
                text = f"*📖 {escape_markdown_v2(technique['name'])}*\n\n"
                text += f"*Description:*\n{escape_markdown_v2(technique['description'])}\n\n"
                text += f"*Category:* `{escape_markdown_v2(technique['category'])}`\n\n"
                text += "*Solutions:*\n"
                solutions = technique.get('solutions', [])
                if not isinstance(solutions, list):
                    solutions = [str(solutions)]
                for i, solution in enumerate(solutions, 1):
                    text += f"{i}\\. {escape_markdown_v2(solution)}\n"

                bot.reply_to(
                    message,
                    text,
                    parse_mode='MarkdownV2'
                )

        except Exception as e:
            bot.reply_to(
                message,
                f"❌ Error: {escape_markdown_v2(str(e))}",
                parse_mode='MarkdownV2'
            )

    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call):
        """Handle callback queries"""
        try:
            if call.data.startswith('describe_'):
                technique_id = call.data.split('_')[1]
                technique = search_engine.get_technique_by_id(technique_id)
                if technique:
                    text = f"*📖 {escape_markdown_v2(technique['name'])}*\n\n"
                    text += f"*Description:*\n{escape_markdown_v2(technique['description'])}\n\n"
                    text += f"*Category:* `{escape_markdown_v2(technique['category'])}`\n\n"
                    text += "*Solutions:*\n"
                    solutions = technique.get('solutions', [])
                    if not isinstance(solutions, list):
                        solutions = [str(solutions)]
                    for i, solution in enumerate(solutions, 1):
                        text += f"{i}\\. {escape_markdown_v2(solution)}\n"
                    markup = types.InlineKeyboardMarkup()
                    markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data="back_to_search"))
                    bot.edit_message_text(
                        text,
                        call.message.chat.id,
                        call.message.message_id,
                        parse_mode='MarkdownV2',
                        reply_markup=markup
                    )
            elif call.data.startswith('category_'):
                category = call.data[9:].replace('_', ' ')
                techniques = search_engine.get_techniques_by_category(category)
                text = f"*🔍 Techniques in {escape_markdown_v2(category)}:*\n\n"
                markup = types.InlineKeyboardMarkup(row_width=2)
                buttons = []
                for technique in techniques:
                    text += f"• `{escape_markdown_v2(technique['name'])}`\n"
                    buttons.append(
                        types.InlineKeyboardButton(
                            f"📖 {technique['name'][:20]}...",
                            callback_data=f"describe_{technique['id']}_category"
                        )
                    )
                markup.add(*buttons)
                markup.add(types.InlineKeyboardButton("⬅️ Back to Categories", callback_data="back_to_list"))
                bot.edit_message_text(
                    text,
                    call.message.chat.id,
                    call.message.message_id,
                    parse_mode='MarkdownV2',
                    reply_markup=markup
                )
            elif call.data == "back_to_menu":
                handle_start_help(call.message)
            elif call.data == "back_to_search":
                bot.delete_message(call.message.chat.id, call.message.message_id)
            elif call.data == "back_to_list":
                handle_list(call.message)
        except Exception as e:
            bot.answer_callback_query(
                call.id,
                f"❌ Error: {escape_markdown_v2(str(e))}",
                show_alert=True
            )

    return bot 