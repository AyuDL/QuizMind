## SQL
Token
	ID uuid
	value string
	purpose string
	expires_at datetime
	used_at datetime
	user_id uuid

Category
	ID uuid
	label string

User
	ID uuid
	last_name string
	first_name string
	username string
	email string
	password password
	birth_date datetime
	created_at datetime
	league_point int
	is_confirmed bool

Quiz_User
	ID uuid
	user_id uuid
	quiz_id uuid
	quiz_point int
	did_at datetime

Quiz
	ID uuid
	title string
	description string
	is_public bool
	created_at datetime
	difficulty string
	user_id uuid
	uploaded_file_id uuid
	category_id uuid

Comment
	ID uuid
	user_id uid
	quiz_id uid
	created_at datetime
	content string

Question
	ID uuid
	title string
	explanation string

Question_Choice
	ID uuid
	content string
	is_true bool
	question_id uuid

Uploaded_file
	ID uuid
	url string
	file_full_name string
	file_custom_name string
	created_at datetime

Badge
	ID uuid
	title string
	content string
	condition_target int

User_Badge
	ID uuid
	obtain_at datetime
	progress int
	badge_id uuid
	user_id uuid

Challenge
	ID uuid
	badge_id uid
	type string

Challenge_User
	ID uuid
	user_id uuid
	challenge_id uuid
	complete bool


## NO SQL

Notes
	ID uuid
	ratting_difficulty int
	ratting_theme int
	ratting_coverage int
	user_id uuid
	quiz_id uuid

{
"ID": "ObjectID (generate by MongoDB)",
  "user_id": "uuid",
  "quiz_id": "uuid",
  "rating_difficulty": "int (0 à 5)",
  "rating_theme": "int (0 à 5)",
  "rating_coverage": "int (0 à 5)",
}