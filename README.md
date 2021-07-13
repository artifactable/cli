# aet

`aet` is a notification service for your dbt project. You can subscribe to alerts for just the models you want to track by simply tagging your dbt models.

```sql
{{
  config(
    tags=[
        'notify:analytics_eng@acme.com',
        'notify:tom@acme.com'
    ]
  )
}}
```

You can also configure alerts for a collection of models from your `dbt_project.yml` file.

```yml
models:
  acme:
    core:
      +tags:
        - notify:analytics_eng@acme.com
        - notify:slas@acme.com
    marketing:
      +tags:
        - notify:marketing_analysts@acme.com
```

## Quickstart

Install with pip.

```
pip install aet
```

Register an account.

```
aet register
```

Then run or test your dbt project or tests as you normally would, and upload your results to the `aet` service to send alerts about any build or test failures.

```bash
# Run your models or tests
dbt run

# Upload your results to send notifications
aet push
```

## Running from a CI suite

To send alerts via a CI process, you'll need to set an environment variable `AET_TOKEN` that contains a token used to authenticate with `aet`'s service.

To find this token, log into your `aet` account with your email and password.

```
aet login
```

Then view the credential details stored in the `~/.aet` folder.

```
cat ~/.aet/user.json
```

You should see a field called `token`, which contains the token you need.

```json
{
  "data": {
    "id": "1",
    "type": "users",
    "attributes": {
      "email": "tom@acme.com",
      
      // This one!
      "token": "94ac5c4e-7ebe-4857-9f8a-c112266b9151",
      "created-at": "2021-07-10T08:50:12.527Z",
      "confirmed-at": null
    }
  }
}
```

Then set that token in your environment. Note that the token will take priority over any value stored in `~/.aet`.

```bash
export AET_TOKEN=94ac5c4e-7ebe-4857-9f8a-c112266b9151
```

You can now send alerts via `aet` without requiring logging in.

```
dbt test && aet push
```

## Reference

Please use the `--help` command for a full list of options.

```
aet --help
```
