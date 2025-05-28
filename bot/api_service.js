const axios = require("axios");

const API_URL = process.env.API_URL ?? "http://127.0.0.1";
const API_PORT = process.env.API_PORT ?? "8000";

const createPost = async (post, author_id) => {
  const { title, description, category, message_id } = post;

  try {
    const {
      data: { _id: category_id },
    } = await axios.get(`${API_URL}:${API_PORT}/categories/name/${category}`);

    await axios.post(`${API_URL}:${API_PORT}/posts/`, {
      _id: "1",
      title,
      description,
      category_id,
      author_id,
      message_id,
      chat_msg_id: "",
      created_at: new Date().toISOString(),
      attachments: [],
      comments: [],
    });
  } catch (err) {}
};

const deletePost = async (message_id, user_id) => {
  try {
    const {
      data: { author_id },
    } = await axios.get(`${API_URL}:${API_PORT}/posts/${message_id}`);

    const {
      data: { role },
    } = await axios.get(`${API_URL}:${API_PORT}/users/${user_id}`);

    if (user_id !== author_id && role !== "admin")
      throw new Error("User cannot delete this post");

    await axios.delete(`${API_URL}:${API_PORT}/posts/${message_id}`);
  } catch (err) {
    console.error(err);
    throw new Error("User cannot delete this post");
  }
};

const getPostByChatMsgId = async (message_id) => {
  try {
    const { data: post } = await axios.get(
      `${API_URL}:${API_PORT}/posts/thread/${message_id}`,
    );
    return post;
  } catch (error) {
    console.log("error");
  }
};

const createUser = async (user) => {
  try {
    await axios.post(`${API_URL}:${API_PORT}/users/`, user);
  } catch (err) {
    console.log("error");
  }
};

const getUser = async (telegram_id) => {
  try {
    const { data: user } = await axios.get(
      `${API_URL}:${API_PORT}/users/${telegram_id}`,
    );
    return user;
  } catch (err) {}
};

const toggleUserAdmin = async (telegram_id) => {
  try {
    const { data: user } = await axios.get(
      `${API_URL}:${API_PORT}/users/${telegram_id}`,
    );

    const role = user.role === "admin" ? "user" : "admin";

    await axios.put(`${API_URL}:${API_PORT}/users/${telegram_id}`, {
      ...user,
      role,
    });
    return role;
  } catch (err) {}
};

const createCategory = async (category) => {
  category = { ...category, _id: 1 };
  try {
    await axios.post(`${API_URL}:${API_PORT}/categories/`, category);
  } catch (err) {}
};

const deleteCategory = async (name) => {
  try {
    await axios.delete(`${API_URL}:${API_PORT}/categories/${name}`);
  } catch (err) {
    console.error(err);
    throw new Error("User cannot delete this category");
  }
};

const updatePostWithAttachment = async (message_id, file) => {
  try {
    const { data: post } = await axios.get(
      `${API_URL}:${API_PORT}/posts/${message_id}`,
    );

    await axios.put(`${API_URL}:${API_PORT}/posts/${message_id}`, {
      ...post,
      attachments: [...post.attachments, { ...file }],
    });
  } catch (err) {
    console.log("error heppened...");
  }
};

const updatePostWithChatMsgId = async (message_id, chat_msg_id) => {
  try {
    const { data: post } = await axios.get(
      `${API_URL}:${API_PORT}/posts/${message_id}`,
    );

    await axios.put(`${API_URL}:${API_PORT}/posts/${message_id}`, {
      ...post,
      chat_msg_id: chat_msg_id.toString(),
    });
  } catch (err) {
    console.log("error heppened...");
  }
};

const updatePostWithComment = async (message_id, comment) => {
  try {
    const { data: post } = await axios.get(
      `${API_URL}:${API_PORT}/posts/thread/${message_id}`,
    );
    console.log(post);

    await axios.put(`${API_URL}:${API_PORT}/posts/${post.message_id}`, {
      ...post,

      comments: [
        ...post.comments,
        { ...comment, timestamp: new Date().toISOString() },
      ],
    });
  } catch (err) {
    console.log("error heppened...");
  }
};

const getLastPostFromUser = async (author_id) => {
  try {
    const { data: post } = await axios.get(
      `${API_URL}:${API_PORT}/posts/last/${author_id}`,
    );

    return post;
  } catch (err) {
    console.log("error heppened...");
  }
};

const getUserPosts = async (author_id) => {
  try {
    const { data: posts } = await axios.get(
      `${API_URL}:${API_PORT}/posts/author/${author_id}`,
    );

    return posts;
  } catch (err) {
    console.log("error heppened...");
  }
};

const getCategories = async () => {
  try {
    const { data: categories } = await axios.get(
      `${API_URL}:${API_PORT}/categories`,
    );
    return categories;
  } catch (err) {
    console.log("error heppened...");
  }
};

module.exports = {
  createPost,
  deletePost,
  createUser,
  createCategory,
  deleteCategory,
  getUser,
  getPostByChatMsgId,
  toggleUserAdmin,
  updatePostWithAttachment,
  updatePostWithChatMsgId,
  updatePostWithComment,
  getLastPostFromUser,
  getUserPosts,
  getCategories,
};
