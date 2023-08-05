from autoai_libs.transformers.exportable import NumpyColumnSelector
from autoai_libs.transformers.exportable import CompressStrings
from autoai_libs.transformers.exportable import NumpyReplaceMissingValues
from autoai_libs.transformers.exportable import NumpyReplaceUnknownValues
from autoai_libs.transformers.exportable import boolean2float
from autoai_libs.transformers.exportable import CatImputer
from autoai_libs.transformers.exportable import CatEncoder
import numpy as np
from autoai_libs.transformers.exportable import float32_transform
from autoai_libs.transformers.exportable import FloatStr2Float
from autoai_libs.transformers.exportable import NumImputer
from autoai_libs.transformers.exportable import OptStandardScaler
from lale.lib.lale import ConcatFeatures
from autoai_libs.transformers.exportable import NumpyPermuteArray
from autoai_libs.cognito.transforms.transform_utils import TA2
import autoai_libs.utils.fc_methods
from autoai_libs.cognito.transforms.transform_utils import FS1
from autoai_libs.cognito.transforms.transform_utils import TA1
from sklearn.linear_model import LogisticRegression
import lale

lale.wrap_imported_operators()
numpy_column_selector_0 = NumpyColumnSelector(
    columns=[0, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
)
compress_strings = CompressStrings(
    compress_type="hash",
    dtypes_list=[
        "char_str", "char_str", "char_str", "char_str", "char_str", "int_num",
        "char_str", "char_str", "int_num", "char_str", "int_num", "char_str",
        "char_str", "int_num", "char_str", "int_num", "char_str", "char_str",
    ],
    missing_values_reference_list=["", "-", "?", float("nan")],
    misslist_list=[
        [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
        [],
    ],
)
numpy_replace_missing_values_0 = NumpyReplaceMissingValues(
    missing_values=[], filling_values=float("nan")
)
numpy_replace_unknown_values = NumpyReplaceUnknownValues(
    filling_values=float("nan"),
    filling_values_list=[
        float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
        float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
        float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
        float("nan"), float("nan"), float("nan"),
    ],
    known_values_list=[
        [
            227259264688753646810077375790908286508,
            253732214910815238134509288111402486722,
            303819144345098626554456011496217223575,
            280353606872939388614315901186094326949,
        ],
        [
            310861434292724266828512742170106879235,
            259078546728323006823621149382123274851,
            241304191515355600141369672905481462228,
            210421363963937264134596964576525922958,
            32212939341074532066845731816970003693,
        ],
        [
            338473629843581165720544432281125239609,
            326781793206258442673692969623843435113,
            272002530391893084684429324616350007975,
            249661578098852569030863268336475104259,
            277452992311061223498548004061740954923,
            337000624133206789825115182809991844205,
            161330870025401753341235738137984802479,
            133401727367742042681318083577551821203,
            260491112873202394519945523636494874646,
            208131593747174447223154626949015695834,
            317093190772141179412539616679296858597,
        ],
        [
            155466114539413991851582417126364895339,
            246789352403109329930648176329125946981,
            295936621451169689699218469248254275361,
            223681476361652455808150317408145666122,
            230715114430321724850934713783197932106,
        ],
        [
            185340558928138909626603812763488190588,
            319328661378046583715176476627492385778,
            263799749086692576083148855705354099872,
            179222502770383138876302755836424893586,
            283364312271660996400883763491949419861,
        ],
        [1, 2, 3, 4, 5, 6],
        [
            52149379001264932068757487059177351405,
            10381015089147753033583386570985939629,
        ],
        [
            90380513159839424205657141466603309780,
            72020144360318906788270974425375628494,
            68186749286663113704472210246844540664,
        ],
        [1, 2, 3, 4, 5],
        [
            184210183797580735197442541762508088723,
            112784645159752486323086095897586579102,
            194064631024616485005022213750224679171,
            230715114430321724850934713783197932106,
        ],
        [
            19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
            35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
            51, 52, 53, 54, 55, 56, 57, 59, 60, 61, 70,
        ],
        [
            251696305476606261219998849299484831626,
            68186749286663113704472210246844540664,
            129843969358953857049997737920307864573,
        ],
        [
            226204649993248704235747196731638161812,
            240703879997496844699455009880498205665,
            243184888600665221836895697954701357177,
        ],
        [1, 2, 3],
        [
            328286527295663582663365503319902632676,
            119641707607939038914465000864290288880,
            283364312271660996400883763491949419861,
            27741019508977055807423991753468819528,
        ],
        [1, 2],
        [
            68186749286663113704472210246844540664,
            220736790854050750400968561922076059550,
        ],
        [
            169662019754859674907370307324476606919,
            220736790854050750400968561922076059550,
        ],
    ],
    missing_values_reference_list=["", "-", "?", float("nan")],
)
cat_imputer = CatImputer(
    strategy="most_frequent",
    missing_values=float("nan"),
    sklearn_version_family="23",
)
cat_encoder = CatEncoder(
    encoding="ordinal",
    categories="auto",
    dtype=np.float64,
    handle_unknown="error",
    sklearn_version_family="23",
)
numpy_column_selector_1 = NumpyColumnSelector(columns=[1, 4])
float_str2_float = FloatStr2Float(
    dtypes_list=["int_num", "int_num"], missing_values_reference_list=[]
)
numpy_replace_missing_values_1 = NumpyReplaceMissingValues(
    missing_values=[], filling_values=float("nan")
)
num_imputer = NumImputer(strategy="median", missing_values=float("nan"))
opt_standard_scaler = OptStandardScaler(
    num_scaler_copy=None,
    num_scaler_with_mean=None,
    num_scaler_with_std=None,
    use_scaler_flag=False,
)
numpy_permute_array = NumpyPermuteArray(
    axis=0,
    permutation_indices=[
        0, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 1, 4,
    ],
)
ta2 = TA2(
    fun=np.add,
    name="sum",
    datatypes1=[
        "intc", "intp", "int_", "uint8", "uint16", "uint32", "uint64", "int8",
        "int16", "int32", "int64", "short", "long", "longlong", "float16",
        "float32", "float64",
    ],
    feat_constraints1=[autoai_libs.utils.fc_methods.is_not_categorical],
    datatypes2=[
        "intc", "intp", "int_", "uint8", "uint16", "uint32", "uint64", "int8",
        "int16", "int32", "int64", "short", "long", "longlong", "float16",
        "float32", "float64",
    ],
    feat_constraints2=[autoai_libs.utils.fc_methods.is_not_categorical],
    col_names=[
        "CheckingStatus", "LoanDuration", "CreditHistory", "LoanPurpose",
        "LoanAmount", "ExistingSavings", "EmploymentDuration",
        "InstallmentPercent", "Sex", "OthersOnLoan",
        "CurrentResidenceDuration", "OwnsProperty", "Age", "InstallmentPlans",
        "Housing", "ExistingCreditsCount", "Job", "Dependents", "Telephone",
        "ForeignWorker",
    ],
    col_dtypes=[
        np.dtype("float32"), np.dtype("float32"), np.dtype("float32"),
        np.dtype("float32"), np.dtype("float32"), np.dtype("float32"),
        np.dtype("float32"), np.dtype("float32"), np.dtype("float32"),
        np.dtype("float32"), np.dtype("float32"), np.dtype("float32"),
        np.dtype("float32"), np.dtype("float32"), np.dtype("float32"),
        np.dtype("float32"), np.dtype("float32"), np.dtype("float32"),
        np.dtype("float32"), np.dtype("float32"),
    ],
)
fs1_0 = FS1(
    cols_ids_must_keep=range(0, 20),
    additional_col_count_to_keep=20,
    ptype="classification",
)
ta1 = TA1(
    fun=np.sqrt,
    name="sqrt",
    datatypes=["numeric"],
    feat_constraints=[
        autoai_libs.utils.fc_methods.is_non_negative,
        autoai_libs.utils.fc_methods.is_not_categorical,
    ],
    col_names=[
        "CheckingStatus", "LoanDuration", "CreditHistory", "LoanPurpose",
        "LoanAmount", "ExistingSavings", "EmploymentDuration",
        "InstallmentPercent", "Sex", "OthersOnLoan",
        "CurrentResidenceDuration", "OwnsProperty", "Age", "InstallmentPlans",
        "Housing", "ExistingCreditsCount", "Job", "Dependents", "Telephone",
        "ForeignWorker", "sum(LoanDuration__LoanAmount)",
        "sum(LoanDuration__Age)", "sum(LoanAmount__Age)",
    ],
    col_dtypes=[
        np.dtype("float32"), np.dtype("float32"), np.dtype("float32"),
        np.dtype("float32"), np.dtype("float32"), np.dtype("float32"),
        np.dtype("float32"), np.dtype("float32"), np.dtype("float32"),
        np.dtype("float32"), np.dtype("float32"), np.dtype("float32"),
        np.dtype("float32"), np.dtype("float32"), np.dtype("float32"),
        np.dtype("float32"), np.dtype("float32"), np.dtype("float32"),
        np.dtype("float32"), np.dtype("float32"), np.dtype("float32"),
        np.dtype("float32"), np.dtype("float32"),
    ],
)
fs1_1 = FS1(
    cols_ids_must_keep=range(0, 20),
    additional_col_count_to_keep=20,
    ptype="classification",
)
logistic_regression = LogisticRegression(
    class_weight="balanced",
    fit_intercept=False,
    intercept_scaling=0.008121901536221943,
    max_iter=385,
    n_jobs=1,
    random_state=33,
    tol=0.00019811038777392076,
)
pipeline = (
    (
        (
            numpy_column_selector_0
            >> compress_strings
            >> numpy_replace_missing_values_0
            >> numpy_replace_unknown_values
            >> boolean2float()
            >> cat_imputer
            >> cat_encoder
            >> float32_transform()
        )
        & (
            numpy_column_selector_1
            >> float_str2_float
            >> numpy_replace_missing_values_1
            >> num_imputer
            >> opt_standard_scaler
            >> float32_transform()
        )
    )
    >> ConcatFeatures()
    >> numpy_permute_array
    >> ta2
    >> fs1_0
    >> ta1
    >> fs1_1
    >> logistic_regression
)