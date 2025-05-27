require("dotenv").config();
const { Bot, GrammyError, HttpError, InlineKeyboard } = require("grammy");

const {
  createPost,
  createUser,
  updatePostWithAttachment,
  updatePostWithChatMsgId,
  updatePostWithComment,
  getLastPostFromUser,
  getCategories,
  toggleUserAdmin,
  getUser,
  createCategory,
  deletePost,
  deleteCategory,
  getUserPosts,
  getPostByChatMsgId,
} = require("./api_service.js");

const bot = new Bot(process.env.BOT_API_KEY);

const CHANNEL_ID = "-1002257726720";
const ANMIN_CHAT_ID = 1278952568;
const COMMENTS_CHAT_ID = -1002648897390;
const TELEGRAM_BOT_ID = 777000;

const userLastCategoryMap = {};
const userLastPostMap = {};
const postsMapChannelToGroup = {};

const sendMessage = async (chat, message, reply_id = null) => {
  return bot.api.sendMessage(chat, message, {
    reply_to_message_id: reply_id,
  });
};

function getPostLink(channelId, messageId) {
  if (typeof channelId === "string" && channelId.startsWith("@")) {
    return `https://t.me/${channelId.slice(1)}/${messageId}`;
  } else if (typeof channelId === "number" || channelId.startsWith("-100")) {
    const id = channelId.toString().replace("-100", "");
    return `https://t.me/c/${id}/${messageId}`;
  }
  return null;
}

function escapeHTML(text) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

const checkIsNotForBot = (ctx) => {
  return [COMMENTS_CHAT_ID, CHANNEL_ID, TELEGRAM_BOT_ID].includes(ctx.from.id);
};

const checkNotIsAdmin = async (id) => {
  const user = await getUser(id);
  return user.role !== "admin";
};

const sendCategoriesKeyboard = async (to) => {
  const categories = await getCategories();
  const rows = categories.map((category) => [
    InlineKeyboard.text(category.name, category.name),
  ]);

  const categoriesKeyboard = InlineKeyboard.from(rows);
  await bot.api.sendMessage(to, "Оберіть категорію", {
    reply_markup: categoriesKeyboard,
  });
};

// bot.api.setMyCommands([
//   { command: "start", description: "Почати роботу" },
//   { command: "new", description: "Створити нове оголошення" },
//   { command: "post", description: "Опублікувати оголошення" },
//   { command: "my", description: "Отримати створенні оголошення" },
//   { command: "remove", description: "Видалити оголошення" },
//   { command: "categories", description: "Отримати доступні категорії" },
// ]);

bot.command("start", async (ctx) => {
  if (checkIsNotForBot(ctx)) return;

  let preMessage = "";
  const oldUser = await getUser(ctx.from.id);
  if (oldUser) {
    preMessage =
      "Здається Ви раніше вже користувались мною. В будь-якому разі радий, що Ви тут.\nНагадаю, ";
  } else {
    const user = {
      name: ctx.from.username || ctx.from.first_name,
      contact: ctx.from.id.toString(),
      role: "user",
    };
    await createUser(user);
    preMessage = "Вітаю! ";
  }

  await ctx.reply(
    preMessage + "Ви можете створити пост за допомогою команди /new",
  );

  // const shareKeyboard = new Keyboard().requestContact("contact").oneTime();

  // await ctx.reply(
  //   "Для початку відкрийте свій контакт, щоб користувачі можги звязатися з Вами",
  //   {
  //     reply_markup: shareKeyboard,
  //   },
  // );
});

// bot.on(":contact", async (ctx) => {
//   await ctx.reply(
//     "Дякуємо, тепер Ви можете створити пост за допомогою команди /new \n\nВкажіть інформацію у наступному вигляді: \nНазва посту \nЙого опис \nКатегорія",
//   );
// });

bot.command("admin", async (ctx) => {
  if (checkIsNotForBot(ctx)) return;

  if (ctx.message.text.split(" ")[1] !== "password") return;

  const role = await toggleUserAdmin(ctx.from.id.toString());
  const map = {
    user: "у ролі звичайного користувача.",
    admin: "адміністратор.",
  };
  await ctx.reply(`Вітаю, тепер Ви ${map[role]}`);
});

bot.command("category", async (ctx) => {
  if (checkIsNotForBot(ctx)) return;
  if (await checkNotIsAdmin(ctx.from.id.toString())) return;

  const category = {
    name: ctx.message.text.split(" ").slice(1).join("_"),
  };
  if (!category.name.trim()) {
    return await ctx.reply("Потрібно вказати назву категорії");
  }
  await createCategory(category);
  const categories = await getCategories();
  await ctx.reply(
    `Категорія "${
      category.name
    }" успішно створена.\nОновлений список категорій: ${categories
      .map((c) => c.name)
      .join(", ")}`,
  );
});

bot.command("delete", async (ctx) => {
  if (checkIsNotForBot(ctx)) return;
  if (await checkNotIsAdmin(ctx.from.id.toString())) return;

  const name = ctx.message.text.split(" ").slice(1).join("_");
  await deleteCategory(name);

  const categories = await getCategories();
  await ctx.reply(
    `Категорія "${name}" успішно видалена.\nОновлений список категорій: ${categories
      .map((c) => c.name)
      .join(", ")}`,
  );
});

bot.command("categories", async (ctx) => {
  if (checkIsNotForBot(ctx)) return;
  if (await checkNotIsAdmin(ctx.from.id.toString())) return;

  const categories = await getCategories();
  if (categories.length === 0)
    return await ctx.reply(
      "Категрій немає, отже користувачі не зможуть створити пости. Додайте категорію за допомогою команди /category назва категорії",
    );

  await ctx.reply(
    `Список категорій: ${categories.map((c) => c.name).join(", ")}`,
  );
});

bot.command("new", async (ctx) => {
  await sendCategoriesKeyboard(ctx.from.id);
});

bot.command("post", async (ctx) => {
  if (checkIsNotForBot(ctx)) return;

  const lines = ctx.message.text.replace("/post", "").trim().split("\n");

  if (lines.length != 2) {
    return ctx.reply("❗️ Введіть два абзаци: Назва, опис");
  }
  const [title, description] = lines;
  const category = userLastCategoryMap[ctx.from.id];

  const user = ctx.from;
  const userLink = `<a href="tg://user?id=${user.id}">${user.username}</a>`;

  const post = `<b>${escapeHTML(title)}</b>\n#${escapeHTML(
    category,
  )}\n\n<i>${escapeHTML(
    description,
  )}</i>\n\n👤 Автор: <span class="tg-spoiler">${userLink}</span>`;

  const message = await ctx.api.sendMessage(CHANNEL_ID, post, {
    parse_mode: "HTML",
  });

  postsMapChannelToGroup[message.message_id] = null;
  userLastPostMap[ctx.message.from.id] = message.message_id;

  await ctx.reply(
    "Пост створено: " + getPostLink(CHANNEL_ID, message.message_id),
  );
  await ctx.reply("Якщо є бажання - надішліть прикріплення");

  await createPost(
    { title, description, category, message_id: message.message_id.toString() },
    ctx.from.id,
  );
});

bot.command("my", async (ctx) => {
  if (checkIsNotForBot(ctx)) return;

  const posts = await getUserPosts(ctx.from.id);

  if (posts.length === 0)
    return await ctx.reply(
      "Опублікованих постів немає, створіть свій перший пост за допомогою команди /new",
    );

  await ctx.reply(
    `Ваші опубліковані пости:\n${posts
      .map((post) => getPostLink(CHANNEL_ID, post.message_id))
      .join("\n")}`,
  );
});

bot.command("remove", async (ctx) => {
  if (checkIsNotForBot(ctx)) return;

  const text = ctx.message.text;
  const regex = /https:\/\/t\.me\/c\/(\d+)\/(\d+)/;
  const match = text.match(regex);

  if (!match) {
    return ctx.reply("Невірний формат посилання.");
  }

  const chatId = `-100${match[1]}`;
  const messageId = Number(match[2]);

  try {
    await deletePost(messageId.toString(), ctx.from.id);
    await ctx.api.deleteMessage(chatId, messageId);
    await ctx.reply("Пост успішно видалено.");
  } catch (error) {
    console.error(error);
    await ctx.reply(
      "На жаль, не вдалося видалити пост. Варто перевіри права доступу або посилання.",
    );
  }
});

bot.on([":photo", ":video"], async (ctx) => {
  if (checkIsNotForBot(ctx)) return;
  const caption = ctx.message.caption || "";
  const to = COMMENTS_CHAT_ID;

  const { message_id: post_id, chat_msg_id: reply_to_message_id } =
    await getLastPostFromUser(ctx.message.from.id);

  if (ctx.message.photo) {
    const photo = ctx.message.photo.at(-1);
    await ctx.api.sendPhoto(to, photo.file_id, {
      caption,
      reply_to_message_id,
    });
  } else if (ctx.message.video) {
    await ctx.api.sendVideo(to, ctx.message.video.file_id, {
      caption,
      reply_to_message_id,
    });
  }

  await ctx.reply(
    "Файл усішно додано до поста.\nТепер можете додати ще фото або ж створити новий пост",
  );

  const photos = ctx.message.photo;
  const biggestPhoto = photos.at(-1);

  const file = {
    file_type: ctx.message.photo ? "photo" : "video",
    url: biggestPhoto.file_id,
  };
  await updatePostWithAttachment(post_id, file);
});

bot.on("msg", async (ctx) => {
  // console.log(JSON.stringify(ctx, null, 2));
  if (ctx.message?.from.id == TELEGRAM_BOT_ID) {
    await updatePostWithChatMsgId(
      ctx.message.forward_from_message_id,
      ctx.message.message_id,
    );
  } else if (ctx.message?.message_thread_id) {
    const comment = {
      user_id: ctx.message.from.id,
      text: ctx.message.text,
    };
    await updatePostWithComment(ctx.message.message_thread_id, comment);

    const { message_id, author_id } = await getPostByChatMsgId(
      ctx.message.message_thread_id,
    );

    await bot.api.sendMessage(
      author_id,
      `Ваш пост ${getPostLink(
        CHANNEL_ID,
        message_id,
      )} щойно отримав новий коментар`,
    );
  }
});

bot.on("callback_query:data", async (ctx) => {
  await ctx.reply(
    "Використовуючи команду /post вкажіть інформацію у наступному вигляді:\n\n/post Назва посту \nЙого опис",
  );
  await ctx.editMessageText(`Обрана категорія: "${ctx.callbackQuery.data}`);
  userLastCategoryMap[ctx.from.id] = ctx.callbackQuery.data;
  await ctx.answerCallbackQuery();
});

bot.catch(async (err) => {
  const { ctx } = err;
  console.error(`Error while handling update ${ctx.update.update_id}:`, err);

  const e = err.error;
  await ctx.reply(e);
  await ctx.reply("Перепрошую, сталася помилка, зверністься до розробника");

  if (e instanceof GrammyError) {
    console.error("A Grammy error occurred:", e.description);
  } else if (e instanceof HttpError) {
    console.error("An HTTP error occurred:", e);
  } else {
    console.error("An unknown error occurred:", e);
  }
});

bot.start();
