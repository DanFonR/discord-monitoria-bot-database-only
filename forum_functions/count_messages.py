from discord import Thread
from tools.checks import check_guild_forum_thread

async def get_users_message_count_in_thread(
            thread_id: int) -> dict[int, int] | dict:
    """Retorna um dicionário com os IDs dos usuários
    e a quantidade de mensagens que cada um enviou em uma thread específica."""

    # Primeiro, tentamos verificar se a thread existe
    thread: (Thread | None)
    was_archived: bool 
    thread, was_archived = await check_guild_forum_thread(thread_id)
    
    # Se não encontramos a thread (arquivada aberta ou não),
    # retornamos um dicionário vazio
    if not thread:
        return {}

    user_message_count: (dict[int, int] | dict) = {}

    # Obtendo todas as mensagens da thread
    # Limite pode ser alterado para evitar sobrecarga
    async for message in thread.history(limit=None):
        if message.author.bot:
            continue  # Ignora bots

        user_id: int = message.author.id
        if user_id not in user_message_count:
            user_message_count[user_id] = 0

        user_message_count[user_id] += 1

    if was_archived:
        await thread.edit(archived=True) # Fechando novamente thread arquivada

    return user_message_count
