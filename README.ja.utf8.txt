Android Application Build Script Extension

Android SDK Toolsから生成されるビルドスクリプト（build.xml）を拡張するスクリプト群を
提供します。

機能：
    ・静的コード解析用のターゲットを追加します。

        ・Checkstyle (http://checkstyle.sourceforge.net/)
        ・FindBugs (http://findbugs.sourceforge.net/)
        ・JavaNCSS (http://www.kclee.de/clemens/java/javancss/)
        ・PMD (http://pmd.sourceforge.net/)
        ・PMD's Copy/Paste Detector (CPD) (http://pmd.sourceforge.net/cpd.html)

    ・テスト用のターゲットを追加します。

        ・テスト結果のレポートをJUnit XML形式で生成できます。
        ・生成されたJUnit XML形式のレポートから、テストの成功、失敗を判定できます。
        ・コードカバレッジレポートをXML形式で生成できます。

動作に必要なソフトウェア：

    ・Android SDK Tools Revision 17以上 (http://developer.android.com/)
    ・Ant 1.8.0以上 (http://ant.apache.org/)
    ・静的コード解析用のターゲットを実行する場合は、その静的コード解析ツール。

sdk_r16ブランチから削除された機能：

    ・コードカバレッジのフィルタリング機能
        ・Android SDK Tools Revision 17から、コードカバレッジのフィルタリング機能が
          搭載されたため削除しました。emma.filterプロパティの設定で
          フィルタリングできます。

初期設定：

    1. アプリケーションプロジェクトのトップディレクトリに、buildと名付けたディレクトリを作り、
       その中にこれらスクリプト、サブディレクトリを入れてください。

    2. build.xmlを開き、<import>タスクを以下の内容に置き換えてください。

        <import file="build/extended_build.xml" />

    3. build.xmlのversion-tagの値を「custom」に変更してください。

    例：

        変更前：
                <!-- version-tag: 1 -->
                <import file="${sdk.dir}/tools/ant/build.xml" />

        変更後：
                <!-- version-tag: custom -->
                <import file="build/extended_build.xml" />

Checkstyle用の設定：

    1. checkstyle-x.x-all.jarをAntのライブラリディレクトリに入れてください。

    2. config/extension.propertiesのcheckstyle.enableの値をtrueに変更してください。

    3. Checkstyleの設定ファイルconfig/checkstyle-config.xmlを必要に応じて編集もしくは
       置き換えてください。

FindBugs用の設定：

    1. FindBugsをexternal/findbugsもしくはそのほか任意のディレクトリに
       インストールしてください。

    2. findbugs-ant.jarをAntのライブラリディレクトリに入れてください。

    3. config/extension.propertiesのfindbugs.enableの値をtrueに変更してください。

    4. config/extension.propertiesのfindbugs.homeの値をFindBugsをインストールした
       ディレクトリに必要があれば変更してください。

    5. FindBugsの除外フィルタconfig/findbugs-exclude-filter.xmlを必要に応じて編集
       もしくは置き換えてください。

JavaNCSS用の設定：

    1. JavaNCSSのlibディレクトリ以下を、Antのライブラリディレクトリに入れてください。

    2. config/extension.propertiesのjavancss.enableの値をtrueに変更してください。

PMD用の設定：

    1. PMDのlibディレクトリ以下を、Antのライブラリディレクトリに入れてください。

    2. config/extension.propertiesのpmd.enableの値をtrueに変更してください。

    3. PMDのルールセットconfig/pmd-rule-set.xml（メインコード向け）、
       config/pmd-test-rule-set.xml（テストコード向け）を必要に応じて編集もしくは
       置き換えてください。

PMD's Copy/Paste Detector (CPD)用の設定

    1. PMDのlibディレクトリ以下を、Antのライブラリディレクトリに入れてください。

    2. config/extension.propertiesのpmd.cpd.enableの値をtrueに変更してください。

テスト用の設定：

    1. テストプロジェクトのbuild.xmlを開き、<import>タスクを以下の内容に置き換えてください。

        <import file="${tested.project.dir}/build/extended_build.xml" />

    2. build.xmlのversion-tagの値を「custom」に変更してください。

    3. config/extension.propertiesのtest.enableの値をtrueに変更してください。

追加されるターゲット：

    「Checkstyle用の設定」のあと：

        checkstyle : Checkstyleを実行し、「reports/checkstyle.txt」として
                     テキスト形式でレポートを生成します。

        checkstyle-xml : Checkstyleを実行し、「reports/checkstyle.xml」として
                         XML形式でレポートを生成します。

        例：

            ant checkstyle
                Antを実行したプロジェクトでCheckstyleを実行し、テキスト形式のレポートを
                生成します。

    「FindBugs用の設定」のあと：

        findbugs : FindBugsを実行し、「reports/findbugs.html」としてHTML形式で
                   レポートを生成します。

        findbugs-xml : FindBugsを実行し、「reports/findbugs.xml」としてXML形式で
                       レポートを生成します。

        例：

            ant findbugs
                Antを実行したプロジェクトでFindBugsを実行し、XML形式のレポートを生成します。

    「JavaNCSS用の設定」のあと：

        javancss : JavaNCSSを実行し、「reports/javancss_metrics.txt」として
                   テキスト形式でレポートを生成します。

        javancss-xml : JavaNCSSを実行し、「reports/javancss_metrics.xml」として
                       XML形式でレポートを生成します。

        例：

            ant javancss
                Antを実行したプロジェクトでJavaNCSSを実行し、テキスト形式のレポートを
                生成します。

    「PMD用の設定」のあと：

        pmd : PMDを実行し、「reports/pmd.html」としてHTML形式でレポートを生成します。

        pmd-xml : PMDを実行し、「reports/pmd.xml」としてXML形式でレポートを生成します。

        例：

            ant pmd
                Antを実行したプロジェクトでPMDを実行し、HTML形式のレポートを生成します。

    「PMD's Copy/Paste Detector (CPD)用の設定」のあと：

        cpd : PMD's Copy/Paste Detectorを実行し、「reports/cpd.txt」として
              テキスト形式でレポートを生成します。

        cpd-xml : PMD's Copy/Paste Detectorを実行し、「reports/cpd.xml」として
                  XML形式でレポートを生成します。

        例：

            ant cpd
                Antを実行したプロジェクトでPMD's Copy/Paste Detectorを実行し、
                テキスト形式のレポートを生成します。

    「テスト用の設定」のあと：

        test-xml : テストを実行し、結果のレポートをJUnit XML形式で生成します。

           ・テスト結果を、テストプロジェクトの「reports/test_result.xml」として
             出力します。

           ・emmaターゲットを同時に指定した場合、「reports/coverage.html」と
             「reports/coverage.xml」としてカバレッジレポートを出力します。

        verify-test-result : JUnit XML形式のレポートをチェックし、もしテストに
                             失敗していれば実行中のビルドも失敗させます。

           ・このターゲットには、test-xmlターゲットで生成したレポートが必要です。

           ・もしテストが成功していた場合、このターゲットは何も行いません。

        例：

            ant test-xml
                テストを実行してテスト結果のレポートをJUnit XML形式で生成します。
                このターゲットを実行する前に、テスト対象のアプリケーションと
                テストアプリケーションがデバイスにインストールされていなければなりません。

            ant debug install test-xml
                テスト対象のアプリケーション、テストアプリケーションをビルドし、両者を
                デバイスにインストールした後、テストを実行してテスト結果のレポートを
                JUnit XML形式で生成します。

            ant debug install test-xml verify-test-result
                テスト対象のアプリケーション、テストアプリケーションをビルドし、両者を
                デバイスにインストールした後、テストを実行してテスト結果のレポートを
                JUnit XML形式で生成します。もしテストが失敗していれば、実行中のAntの
                ビルドを失敗させます。

            ant emma debug install test-xml
                テスト対象のアプリケーション、テストアプリケーションをビルドし、両者を
                デバイスにインストールした後、テストを実行してテスト結果のレポートを
                JUnit XML形式で生成します。またHTML形式とXML形式でカバレッジレポートを
                生成します。
