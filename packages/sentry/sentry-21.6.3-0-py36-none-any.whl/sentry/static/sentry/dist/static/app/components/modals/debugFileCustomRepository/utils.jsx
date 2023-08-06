import { __assign, __read, __rest } from "tslib";
import ExternalLink from 'app/components/links/externalLink';
import { AWS_REGIONS, DEBUG_SOURCE_CASINGS, DEBUG_SOURCE_LAYOUTS, } from 'app/data/debugFileSources';
import { t, tct } from 'app/locale';
function objectToChoices(obj) {
    return Object.entries(obj).map(function (_a) {
        var _b = __read(_a, 2), key = _b[0], value = _b[1];
        return [key, t(value)];
    });
}
var commonFields = {
    id: {
        name: 'id',
        type: 'hidden',
        required: true,
        defaultValue: function () { return Math.random().toString(36).substring(2); },
    },
    name: {
        name: 'name',
        type: 'string',
        required: true,
        label: t('Name'),
        placeholder: t('New Repository'),
        help: t('A display name for this repository'),
    },
    // filters are explicitly not exposed to the UI
    layoutType: {
        name: 'layout.type',
        type: 'select',
        label: t('Directory Layout'),
        help: t('The layout of the folder structure.'),
        defaultValue: 'native',
        choices: objectToChoices(DEBUG_SOURCE_LAYOUTS),
    },
    layoutCasing: {
        name: 'layout.casing',
        type: 'select',
        label: t('Path Casing'),
        help: t('The case of files and folders.'),
        defaultValue: 'default',
        choices: objectToChoices(DEBUG_SOURCE_CASINGS),
    },
    prefix: {
        name: 'prefix',
        type: 'string',
        label: 'Root Path',
        placeholder: '/',
        help: t('The path at which files are located within this repository.'),
    },
    separator: {
        name: '',
        type: 'separator',
    },
};
var httpFields = {
    url: {
        name: 'url',
        type: 'url',
        required: true,
        label: t('Download Url'),
        placeholder: 'https://msdl.microsoft.com/download/symbols/',
        help: t('Full URL to the symbol server'),
    },
    username: {
        name: 'username',
        type: 'string',
        required: false,
        label: t('User'),
        placeholder: 'admin',
        help: t('User for HTTP basic auth'),
    },
    password: {
        name: 'password',
        type: 'string',
        required: false,
        label: t('Password'),
        placeholder: 'open-sesame',
        help: t('Password for HTTP basic auth'),
    },
};
var s3Fields = {
    bucket: {
        name: 'bucket',
        type: 'string',
        required: true,
        label: t('Bucket'),
        placeholder: 's3-bucket-name',
        help: t('Name of the S3 bucket. Read permissions are required to download symbols.'),
    },
    region: {
        name: 'region',
        type: 'select',
        required: true,
        label: t('Region'),
        help: t('The AWS region and availability zone of the bucket.'),
        choices: AWS_REGIONS.map(function (_a) {
            var _b = __read(_a, 2), k = _b[0], v = _b[1];
            return [
                k,
                <span key={k}>
        <code>{k}</code> {v}
      </span>,
            ];
        }),
    },
    accessKey: {
        name: 'access_key',
        type: 'string',
        required: true,
        label: t('Access Key ID'),
        placeholder: 'AKIAIOSFODNN7EXAMPLE',
        help: tct('Access key to the AWS account. Credentials can be managed in the [link].', {
            link: (<ExternalLink href="https://console.aws.amazon.com/iam/">
            IAM console
          </ExternalLink>),
        }),
    },
    secretKey: {
        name: 'secret_key',
        type: 'string',
        required: true,
        label: t('Secret Access Key'),
        placeholder: 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
    },
};
var gcsFields = {
    bucket: {
        name: 'bucket',
        type: 'string',
        required: true,
        label: t('Bucket'),
        placeholder: 'gcs-bucket-name',
        help: t('Name of the GCS bucket. Read permissions are required to download symbols.'),
    },
    clientEmail: {
        name: 'client_email',
        type: 'email',
        required: true,
        label: t('Client Email'),
        placeholder: 'user@project.iam.gserviceaccount.com',
        help: t('Email address of the GCS service account.'),
    },
    privateKey: {
        name: 'private_key',
        type: 'string',
        required: true,
        multiline: true,
        autosize: true,
        maxRows: 5,
        rows: 3,
        label: t('Private Key'),
        placeholder: '-----BEGIN PRIVATE KEY-----\n[PRIVATE-KEY]\n-----END PRIVATE KEY-----',
        help: tct('The service account key. Credentials can be managed on the [link].', {
            link: (<ExternalLink href="https://console.cloud.google.com/project/_/iam-admin">
          IAM &amp; Admin Page
        </ExternalLink>),
        }),
    },
};
export function getFormFields(type) {
    switch (type) {
        case 'http':
            return [
                commonFields.id,
                commonFields.name,
                commonFields.separator,
                httpFields.url,
                httpFields.username,
                httpFields.password,
                commonFields.separator,
                commonFields.layoutType,
                commonFields.layoutCasing,
            ];
        case 's3':
            return [
                commonFields.id,
                commonFields.name,
                commonFields.separator,
                s3Fields.bucket,
                s3Fields.region,
                s3Fields.accessKey,
                s3Fields.secretKey,
                commonFields.separator,
                commonFields.prefix,
                commonFields.layoutType,
                commonFields.layoutCasing,
            ];
        case 'gcs':
            return [
                commonFields.id,
                commonFields.name,
                commonFields.separator,
                gcsFields.bucket,
                gcsFields.clientEmail,
                gcsFields.privateKey,
                commonFields.separator,
                commonFields.prefix,
                commonFields.layoutType,
                commonFields.layoutCasing,
            ];
        default:
            return undefined;
    }
}
export function getInitialData(sourceConfig) {
    var _a;
    if (!sourceConfig) {
        return undefined;
    }
    if (sourceConfig.layout) {
        var layout = sourceConfig.layout, initialData = __rest(sourceConfig, ["layout"]);
        var casing = layout.casing, type = layout.type;
        return __assign(__assign({}, initialData), (_a = {}, _a['layout.casing'] = casing, _a['layout.type'] = type, _a));
    }
    return sourceConfig;
}
//# sourceMappingURL=utils.jsx.map