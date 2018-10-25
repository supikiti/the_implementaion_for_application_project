# the-implementaion-for-application_project
応用プロジェクトDのNT班の実装です. 

## 実行方法
以下のコードを実行することで, 総電力(kWh)/36(円) - 総運転費 - 4億 * 償却費(円/台)が出力されます.
```bash
$ python main.py
```

### 内容
#### environment.py
各種環境変数を格納するclass

#### ships.py
船class

#### windfarm.py
風力発電class

#### ship_plan.py
船classをスケジューリングするclass

#### windfarm_state.py
風車の状態をまとめるclass

#### main.py
船と風車の総状態を時間ステップごとに更新する
