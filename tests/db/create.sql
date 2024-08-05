CREATE TABLE allure_tekg (
                             uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                             historyid VARCHAR,
                             fullname VARCHAR,
                             links JSON,
                             labels JSON,
                             name VARCHAR,
                             status VARCHAR,
                             statusdetails JSON,
                             stage VARCHAR,
                             attachments JSON,
                             parameters JSON,
                             start TIMESTAMPTZ,
                             stop TIMESTAMPTZ
);


CREATE TABLE test_steps (
                            id SERIAL PRIMARY KEY,
                            step_name VARCHAR,
                            step_description VARCHAR,
                            test_record_uuid UUID REFERENCES allure_tekg(uuid)
);

CREATE TABLE Container (
                           uuid UUID PRIMARY KEY,
                           name VARCHAR(255) NOT NULL,
                           children UUID[],
                           befores UUID[],
                           afters UUID[],
                           start BIGINT NOT NULL,
                           stop BIGINT NOT NULL
);