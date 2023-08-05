import logging
import os
from os.path import getsize
from shutil import copyfile

from django.conf import settings
from django.core.files import File
from django.db.models import BinaryField, BigIntegerField, CharField, TextField
from django.forms import model_to_dict

from isc_common import delAttr, setAttr
from isc_common.common.UploadItemEx import UploadItemEx
from isc_common.fields.files import FileFieldEx
from isc_common.fields.name_field import NameField
from isc_common.http.DSRequest import DSRequest
from isc_common.managers.common_managet_with_lookup_fields import CommonManagetWithLookUpFieldsManager, CommonManagetWithLookUpFieldsQuerySet
from isc_common.models.audit import AuditModel

logger = logging.getLogger(__name__)


class CryptoQuerySet(CommonManagetWithLookUpFieldsQuerySet):

    def delete(self):
        for item in self:
            Crypto_file.remove_file(item=item)
        return super().delete()


class CryptoManager(CommonManagetWithLookUpFieldsManager):
    def createFromRequest(self, request, function=None):
        request = DSRequest(request=request)
        data = request.get_data()
        _data = data.copy()
        for key in data:
            if key.find('__') != -1:
                delAttr(_data, key)
        delAttr(_data, 'form')
        if data.get('id') or not data.get('real_name'):
            delAttr(_data, 'id')
            res = super().filter(id=data.get('id')).update(**_data)
            res = model_to_dict(res[0])
            delAttr(res, 'attfile')
            delAttr(res, 'form')
            data.update(res)
        return data

    def updateFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()
        delAttr(data, 'form')
        super().filter(id=request.get_id()).update(**data)
        return data

    def get_queryset(self):
        return CryptoQuerySet(self.model, using=self._db)


class Crypto_file(AuditModel):
    attfile = FileFieldEx(verbose_name='Файл', max_length=255)
    file_store = CharField(verbose_name='Каталог хранения файла', max_length=255, null=True, blank=True)
    format = NameField(verbose_name='Формат файла')
    key = BinaryField(max_length=200, null=True, blank=True)
    mime_type = NameField(verbose_name='MIME тип файла файла')
    real_name = TextField(verbose_name='Первоначальное имя файла', db_index=True, unique=True)
    size = BigIntegerField(verbose_name='Размер файла', default=0)

    object = CryptoManager()

    @property
    def olnly_real_file_name(self):
        ls = self.real_name.split('\\')
        return ls[len(ls) - 1]

    @classmethod
    def exists(cls, filename):
        if isinstance(settings.REPLACE_FILE_PATH, dict):
            for key, value in settings.REPLACE_FILE_PATH.items():
                filename = filename.replace(key, value)
        res = os.path.exists(filename)
        if res is False:
            logger.debug(f'file: {filename} not exists.')
        return filename, res

    @classmethod
    def check_file(cls, attfile):
        if attfile is None or attfile == '':
            return False, attfile
        else:
            filename = str(attfile)

            filename, res = cls.exists(filename)
            if res is True:
                if getsize(filename) == 0:
                    return filename, False
            return filename, res

    @classmethod
    def remove_file(cls, item):
        old_file_store = item.file_store
        file_path = item.attfile.name

        if old_file_store:
            file_path = file_path.replace(old_file_store, settings.FILES_STORE)

        if isinstance(settings.REPLACE_FILE_PATH, dict):
            for key, value in settings.REPLACE_FILE_PATH.items():
                file_path = file_path.replace(key, value)

        if file_path:
            if os.altsep:
                file_path = file_path.replace(os.altsep, os.sep)

            if os.path.exists(file_path):
                res = os.remove(file_path)
                logger.debug(f'Removed file: {file_path}')
            else:
                logger.warning(f'Removed file: {file_path} not finded.')

    @classmethod
    def copy_file(cls, uploadItemEx):
        from isc_common.models.images import Images

        if os.path.exists(uploadItemEx.real_file_name):
            copyfile(src=uploadItemEx.real_file_name, dst=uploadItemEx.full_path)
        else:
            if uploadItemEx.tmp_file_name is not None and os.path.exists(uploadItemEx.tmp_file_name):
                copyfile(src=uploadItemEx.tmp_file_name, dst=uploadItemEx.full_path)

        res = cls.objects.getOptional(real_name=uploadItemEx.real_file_name)
        if res is not None:
            return res, False

        with open(uploadItemEx.full_path, 'rb') as src:
            fileObj = File(src)

            defaults=dict(
                attfile=fileObj,
                file_store=uploadItemEx.get_path(fileObj.name),
                format=uploadItemEx.file_format,
                mime_type=uploadItemEx.file_mime_type,
                size=uploadItemEx.file_size,
                real_name=uploadItemEx.real_file_name,
            )

            if issubclass(cls, Images):
                setAttr(defaults, 'image_type', uploadItemEx.image_type)

            res, created = cls.objects.update_or_create(
                id=uploadItemEx.id,
                defaults=defaults
            )

        if uploadItemEx.tmp_file_name is not None and os.path.exists(uploadItemEx.tmp_file_name):
            os.remove(uploadItemEx.tmp_file_name)
            os.remove(uploadItemEx.full_path)

        return res, created

    @classmethod
    def get_action(cls, res, item):
        action = None

        if res.size is None or res.size == 0 or not os.path.exists(str(res.attfile)):
            action = 'create'
        elif res.size != item.file_size:
            action = 'update'
        return action

    @classmethod
    def create_update(cls, **kwargs):
        uploadItemEx = UploadItemEx(**kwargs)

        try:
            if uploadItemEx.id is not None:
                res = cls.objects.get(id=uploadItemEx.id)
                action = cls.get_action(res=res, item=uploadItemEx)
            else:
                if uploadItemEx.real_file_name is None:
                    raise Exception('Must be real_file_name or id')
                else:
                    res = cls.objects.get(real_name=uploadItemEx.real_file_name)

                action = cls.get_action(res=res, item=uploadItemEx)

            if action is not None:
                if action == 'update':
                    cls.remove_file(item=res)

                return cls.copy_file(uploadItemEx=uploadItemEx)
            else:
                return None, None

        except cls.DoesNotExist:
            return cls.copy_file(uploadItemEx=uploadItemEx)

    def __str__(self):
        return f"{self.real_name}"

    class Meta:
        abstract = True
