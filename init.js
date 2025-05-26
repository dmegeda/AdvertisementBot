db.createCollection("users", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["_id", "name", "contact", "role"],
            properties: {
                _id: { bsonType: "int" },
                name: { bsonType: "string" },
                contact: { bsonType: "string" },
                role: { enum: ["user", "admin"] }
            }
        }
    }
});

db.createCollection("categories", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["_id", "name"],
            properties: {
                _id: { bsonType: "int" },
                name: { bsonType: "string" }
            }
        }
    }
});

db.createCollection("posts", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["_id", "title", "description", "category_id", "author_id", "created_at", "attachments", "comments"],
            properties: {
                _id: { bsonType: "int" },
                title: { bsonType: "string" },
                description: { bsonType: "string" },
                category_id: { bsonType: "int" },
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
