db.createCollection("users", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["name", "contact", "role", "registered_at"],
            properties: {
                name: { bsonType: "string" },
                contact: { bsonType: "string" },
                role: { enum: ["user", "admin"] },
                registered_at: { bsonType: "date" }
            }
        }
    }
});

db.createCollection("categories", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["_id", "description", "icon"],
            properties: {
                _id: { bsonType: "string" },
                description: { bsonType: "string" },
                icon: { bsonType: "string" }
            }
        }
    }
});

db.createCollection("posts", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["title", "description", "category_id", "author_id", "created_at", "attachments", "comments"],
            properties: {
                title: { bsonType: "string" },
                description: { bsonType: "string" },
                category_id: { bsonType: "string" },
                author_id: { bsonType: "int" },
                created_at: { bsonType: "date" },
                attachments: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        required: ["file_type", "url"],
                        properties: {
                            file_type: { bsonType: "string" },
                            url: { bsonType: "string" }
                        }
                    }
                },
                comments: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        required: ["user_id", "text", "timestamp"],
                        properties: {
                            user_id: { bsonType: "int" },
                            text: { bsonType: "string" },
                            timestamp: { bsonType: "date" }
                        }
                    }
                }
            }
        }
    }
});

db.posts.createIndex({ title: "text", description: "text" });
db.posts.createIndex({ category_id: 1 });
db.posts.createIndex({ created_at: -1 });
db.posts.createIndex({ author_id: 1 });
