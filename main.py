"""
AstrBot 塔罗牌插件
功能：每日抽牌、塔罗占卜（调用 LLM 解读）
作者：YourName
版本：1.0.1
"""

import random
import hashlib
import os
import json
from datetime import datetime
from typing import List, Dict, Any

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import astrbot.api.message_components as Comp


@register("astrbot_plugin_tarot", "塔罗牌占卜插件", "1.0.1", "https://github.com/yourname/astrbot_plugin_tarot")
class TarotPlugin(Star):
    """塔罗牌占卜插件"""
    
    def __init__(self, context: Context, config: dict = None):
        """
        初始化插件
        
        Args:
            context: AstrBot 上下文
            config: 插件配置
        """
        super().__init__(context)
        self.config = config or {}
        
        # 获取插件所在目录
        self.plugin_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 加载牌面信息
        self.card_info = self._load_card_info()
        
        # 大阿尔克那牌数量
        self.major_arcana_count = 22
        
        logger.info("[塔罗牌] 插件初始化完成")
    
    def _load_card_info(self) -> List[Dict[str, Any]]:
        """
        加载塔罗牌信息 JSON 文件
        
        Returns:
            牌面信息列表
        """
        card_info_path = os.path.join(self.plugin_dir, "CardInfo.json")
        try:
            with open(card_info_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"[塔罗牌] 成功加载 {len(data)} 张牌面信息")
            return data
        except FileNotFoundError:
            logger.error(f"[塔罗牌] 未找到牌面信息文件：{card_info_path}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"[塔罗牌] 牌面信息文件格式错误：{e}")
            return []
    
    def _generate_seed(self, user_id: str, date_str: str) -> int:
        """
        根据用户 ID 和日期生成确定性种子
        
        Args:
            user_id: 用户 ID（QQ 号）
            date_str: 日期字符串（YYYY-MM-DD）
        
        Returns:
            整数种子值
        """
        seed_string = f"{user_id}_{date_str}"
        hash_object = hashlib.sha256(seed_string.encode('utf-8'))
        seed = int(hash_object.hexdigest(), 16) % (2 ** 32)
        return seed
    
    def _get_card_image_path(self, card_index: int) -> str:
        """
        获取牌面图片路径
        
        Args:
            card_index: 牌的序号（0-21）
        
        Returns:
            图片文件路径，不存在则返回 None
        """
        image_dir = os.path.join(self.plugin_dir, "images")
        image_path = os.path.join(image_dir, f"{card_index}.png")
        
        if not os.path.exists(image_path):
            logger.warning(f"[塔罗牌] 图片不存在：{image_path}")
            return None
        return image_path
    
    def _draw_card(self, seed: int) -> Dict[str, Any]:
        """
        抽取一张塔罗牌
        
        Args:
            seed: 随机种子
        
        Returns:
            包含牌面信息的字典
        """
        random.seed(seed)
        
        # 抽取牌序号（0-21）
        card_index = random.randint(0, self.major_arcana_count - 1)
        
        # 抽取正逆位（0=正位，1=逆位）
        is_reversed = random.randint(0, 1) == 1
        
        # 获取牌面信息
        card_data = self.card_info[card_index] if card_index < len(self.card_info) else {}
        
        return {
            "index": card_index,
            "name": card_data.get("名称", f"未知牌{card_index}"),
            "description": card_data.get("牌面描述", ""),
            "upright_meaning": card_data.get("正位喻意", ""),
            "reversed_meaning": card_data.get("逆位喻意", ""),
            "is_reversed": is_reversed,
            "position": "逆位" if is_reversed else "正位"
        }
    
    def _draw_multiple_cards(self, seed: int, count: int, question: str) -> List[Dict[str, Any]]:
        """
        抽取多张塔罗牌（用于占卜）
        
        Args:
            seed: 随机种子
            count: 抽取数量（1-3）
            question: 占卜问题（用于影响抽牌）
        
        Returns:
            牌面信息列表
        """
        cards = []
        
        # 将问题加入种子，使同一问题每次结果一致
        question_seed = hashlib.sha256(question.encode('utf-8')).hexdigest()
        combined_seed = seed + int(question_seed[:8], 16)
        
        random.seed(combined_seed)
        
        # 生成不重复的牌序号
        available_indices = list(range(self.major_arcana_count))
        
        for i in range(count):
            if not available_indices:
                break
            
            card_index = random.choice(available_indices)
            available_indices.remove(card_index)
            
            is_reversed = random.randint(0, 1) == 1
            
            card_data = self.card_info[card_index] if card_index < len(self.card_info) else {}
            
            cards.append({
                "index": card_index,
                "name": card_data.get("名称", f"未知牌{card_index}"),
                "description": card_data.get("牌面描述", ""),
                "upright_meaning": card_data.get("正位喻意", ""),
                "reversed_meaning": card_data.get("逆位喻意", ""),
                "is_reversed": is_reversed,
                "position": "逆位" if is_reversed else "正位",
                "draw_order": i + 1
            })
        
        return cards
    
    def _build_daily_card_message(self, card: Dict[str, Any]) -> str:
        """
        构建每日抽牌消息文本
        
        Args:
            card: 牌面信息字典
        
        Returns:
            格式化消息文本
        """
        meaning = card["reversed_meaning"] if card["is_reversed"] else card["upright_meaning"]
        
        message = (
            f"🔮 ━━━━━━━━━━━━━━━━\n"
            f"✨ 今日塔罗牌 ✨\n"
            f"━━━━━━━━━━━━━━━━\n\n"
            f"📇 序号：{card['index']}\n"
            f"🏷️ 牌名：{card['name']}\n"
            f"🔄 状态：{card['position']}\n\n"
            f"📜 牌面描述：\n{card['description']}\n\n"
            f"💡 喻意：\n{meaning}\n\n"
            f"━━━━━━━━━━━━━━━━\n"
            f"🌟 祝你今天好运！"
        )
        return message
    
    def _build_divination_prompt(self, question: str, cards: List[Dict[str, Any]]) -> str:
        """
        构建 LLM 解读提示词
        
        Args:
            question: 用户占卜问题
            cards: 抽取的牌面列表
        
        Returns:
            LLM 提示词
        """
        cards_info = ""
        for i, card in enumerate(cards):
            meaning = card["reversed_meaning"] if card["is_reversed"] else card["upright_meaning"]
            position_desc = "逆位" if card["is_reversed"] else "正位"
            cards_info += f"\n{i+1}. {card['name']}（{position_desc}）\n   喻意：{meaning}\n"
        
        prompt = (
            f"你是一位专业的塔罗牌占卜师，请根据以下抽取的塔罗牌为用户的问题进行解读。\n\n"
            f"🔮 用户问题：{question}\n\n"
            f"🎴 抽取的牌面：{cards_info}\n\n"
            f"请按照以下格式进行解读：\n"
            f"1. 先简要说明这个牌阵的含义\n"
            f"2. 逐一解读每张牌在当前位置的意义\n"
            f"3. 综合所有牌面给出整体建议\n"
            f"4. 语气要温和、专业，给予积极的指引\n\n"
            f"解读内容："
        )
        return prompt
    
    @filter.command("抽取塔罗牌")
    async def daily_tarot(self, event: AstrMessageEvent):
        """
        每日抽牌指令
        根据用户 QQ 号 + 当前日期生成种子，抽取一张牌
        """
        try:
            # 获取用户 ID 和当前日期
            user_id = event.get_sender_id()
            today = datetime.now().strftime("%Y-%m-%d")
            
            # 生成种子并抽牌
            seed = self._generate_seed(user_id, today)
            card = self._draw_card(seed)
            
            logger.info(f"[塔罗牌] 用户 {user_id} 抽取每日牌：{card['name']} ({card['position']})")
            
            # 构建消息
            message_text = self._build_daily_card_message(card)
            
            # 获取牌面图片
            image_path = self._get_card_image_path(card["index"])
            
            if image_path and os.path.exists(image_path):
                # 发送图片 + 文字（使用正确的 Comp 导入方式）
                chain = [
                    Comp.Image.fromFileSystem(image_path),
                    Comp.Plain(f"\n{message_text}")
                ]
                yield event.chain_result(chain)
            else:
                # 仅发送文字
                yield event.plain_result(message_text)
                
        except Exception as e:
            logger.error(f"[塔罗牌] 每日抽牌失败：{e}")
            yield event.plain_result("❌ 抽牌时发生错误，请稍后再试。")
    
    @filter.command("塔罗占卜")
    async def tarot_divination(self, event: AstrMessageEvent, question: str = ""):
        """
        塔罗占卜指令
        根据问题抽取 1-3 张牌，并调用 LLM 进行解读
        
        Args:
            question: 占卜问题
        """
        try:
            # 检查是否有占卜问题
            if not question or len(question.strip()) < 2:
                yield event.plain_result(
                    "🔮 请提供您要占卜的问题~\n"
                    "用法：塔罗占卜 + 您的问题\n"
                    "例如：塔罗占卜 我最近的运势如何"
                )
                return
            
            # 获取用户 ID 和当前日期
            user_id = event.get_sender_id()
            today = datetime.now().strftime("%Y-%m-%d")
            
            # 根据问题长度决定抽牌数量（简单问题 1 张，复杂问题 3 张）
            card_count = 1 if len(question) <= 10 else 3
            
            # 生成种子并抽牌
            seed = self._generate_seed(user_id, today)
            cards = self._draw_multiple_cards(seed, card_count, question)
            
            logger.info(f"[塔罗牌] 用户 {user_id} 进行占卜，问题：{question[:20]}...，抽取{len(cards)}张牌")
            
            # 构建牌面展示消息
            cards_display = ""
            for card in cards:
                cards_display += f"🎴 {card['name']}（{card['position']}）\n"
            
            initial_message = (
                f"🔮 ━━━━━━━━━━━━━━━━\n"
                f"✨ 塔罗占卜 ✨\n"
                f"━━━━━━━━━━━━━━━━\n\n"
                f"📝 问题：{question}\n\n"
                f"🎴 抽取的牌：\n{cards_display}\n\n"
                f"⏳ 正在为您解读牌意..."
            )
            
            # 先发送牌面信息
            yield event.plain_result(initial_message)
            
            # 调用 LLM 进行解读
            try:
                # 获取当前会话的聊天模型 ID
                umo = event.unified_msg_origin
                provider_id = await self.context.get_current_chat_provider_id(umo=umo)
                
                # 构建提示词
                prompt = self._build_divination_prompt(question, cards)
                
                # 调用 LLM
                llm_resp = await self.context.llm_generate(
                    chat_provider_id=provider_id,
                    prompt=prompt
                )
                
                interpretation = llm_resp.completion_text
                
                # 发送解读结果
                result_message = (
                    f"━━━━━━━━━━━━━━━━\n"
                    f"🌟 牌意解读 🌟\n"
                    f"━━━━━━━━━━━━━━━━\n\n"
                    f"{interpretation}\n\n"
                    f"━━━━━━━━━━━━━━━━\n"
                    f"💫 以上解读仅供参考，命运掌握在自己手中~"
                )
                
                yield event.plain_result(result_message)
                
            except Exception as llm_error:
                logger.error(f"[塔罗牌] LLM 解读失败：{llm_error}")
                
                # LLM 失败时提供基础解读
                fallback_message = (
                    f"━━━━━━━━━━━━━━━━\n"
                    f"🌟 基础解读 🌟\n"
                    f"━━━━━━━━━━━━━━━━\n\n"
                )
                
                for card in cards:
                    meaning = card["reversed_meaning"] if card["is_reversed"] else card["upright_meaning"]
                    fallback_message += f"🎴 {card['name']}（{card['position']}）\n{meaning}\n\n"
                
                fallback_message += (
                    f"━━━━━━━━━━━━━━━━\n"
                    f"⚠️ 详细解读暂时无法生成，请稍后再试。\n"
                    f"💫 命运掌握在自己手中~"
                )
                
                yield event.plain_result(fallback_message)
                
        except Exception as e:
            logger.error(f"[塔罗牌] 占卜失败：{e}")
            yield event.plain_result("❌ 占卜时发生错误，请稍后再试。")
    
    @filter.command("塔罗帮助")
    async def tarot_help(self, event: AstrMessageEvent):
        """
        显示帮助信息
        """
        help_message = (
            "🔮 ━━━━━━━━━━━━━━━━\n"
            "✨ 塔罗牌插件帮助 ✨\n"
            "━━━━━━━━━━━━━━━━\n\n"
            "📌 可用指令：\n\n"
            "1️⃣ 抽取塔罗牌\n"
            "   每日抽取一张塔罗牌\n"
            "   每人每天结果固定\n\n"
            "2️⃣ 塔罗占卜 + 问题\n"
            "   针对具体问题进行占卜\n"
            "   自动抽取 1-3 张牌并解读\n"
            "   例：塔罗占卜 我最近的财运如何\n\n"
            "3️⃣ 塔罗帮助\n"
            "   显示本帮助信息\n\n"
            "━━━━━━━━━━━━━━━━\n"
            "🌙 愿星辰指引你的道路~"
        )
        yield event.plain_result(help_message)
    
    async def terminate(self):
        """
        插件卸载/停用时调用
        """
        logger.info("[塔罗牌] 插件已终止")